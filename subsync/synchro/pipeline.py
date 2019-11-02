import gizmo
from subsync.synchro import speech
from subsync.settings import settings
from subsync.data import languages
from subsync.error import Error
import math

import logging
logger = logging.getLogger(__name__)


class BasePipeline(object):
    def __init__(self, stream, runCb=None):
        self.demux = gizmo.Demux(stream.path, runCb)
        self.extractor = gizmo.Extractor(self.demux)

        self.duration = self.demux.getDuration()
        self.timeWindow = [0, self.duration]

        self.done = False
        self.eosCallback = lambda: None

        def eos():
            logger.info('job terminated')
            self.done = True
            self.eosCallback()

        self.extractor.connectEosCallback(eos)

    def destroy(self):
        self.extractor.connectEosCallback(None)
        self.extractor.connectErrorCallback(None)
        self.extractor.stop()

    def selectTimeWindow(self, begin, end, start=None):
        if end > self.duration:
            end = self.duration
        if begin > end:
            begin = end
        self.timeWindow = (begin, end)
        if start == None:
            start = begin
        self.extractor.selectTimeWindow(start, end)

    def start(self, threadName=None):
        self.extractor.start(threadName=threadName)

    def stop(self):
        self.extractor.stop()

    def isRunning(self):
        return self.extractor.isRunning()

    def getProgress(self):
        if self.duration:
            pos = self.demux.getPosition()
            if math.isclose(pos, 0.0):
                pos = self.timeWindow[0]
            if self.timeWindow[1] > self.timeWindow[0]:
                return (pos - self.timeWindow[0]) / (self.timeWindow[1] - self.timeWindow[0])

    def getPosition(self):
        return max(self.timeWindow[0], min(self.demux.getPosition(), self.timeWindow[1]))

    def connectErrorCallback(self, cb):
        self.extractor.connectErrorCallback(cb)

    def connectEosCallback(self, cb):
        self.eosCallback = cb


class SubtitlePipeline(BasePipeline):
    def __init__(self, stream, runCb=None):
        ''' Speech recognition pipeline:

        Demux --> SpeechDec  --[words]--> {NgramSplitter} --[words]--> ...
        '''

        super().__init__(stream, runCb)
        self.dec = gizmo.SubtitleDec()
        self.dec.setMinWordLen(settings().minWordLen)
        self.ngramSplitter = None
        self.sink = self.dec

        langInfo = stream.lang and languages.get(code3=stream.lang.lower())
        if langInfo:
            if langInfo.rightToLeft:
                logger.info('switching to right-to-left for file "%s"', stream.path)
                self.dec.setRightToLeft(True)

            if langInfo.ngrams:
                logger.info('switching to %i-gram for file "%s"', langInfo.ngrams, stream.path)
                self.dec.setMinWordLen(langInfo.ngrams)
                self.ngramSplitter = gizmo.NgramSplitter(langInfo.ngrams)
                self.dec.addWordsListener(self.ngramSplitter.pushWord)
                self.sink = self.ngramSplitter

        if stream.enc != None:
            self.dec.setEncoding(stream.enc)

        self.demux.connectDec(self.dec, stream.no)

    def destroy(self):
        super().destroy()
        self.dec.removeWordsListener()
        self.dec.removeSubsListener()
        self.sink.removeWordsListener()

    def addWordsListener(self, listener):
        self.sink.addWordsListener(listener)

    def removeWordsListener(self, listener=None):
        return self.sink.removeWordsListener(listener)

    def getRawWordsSource(self):
        return self.dec

    def addSubsListener(self, listener):
        self.dec.addSubsListener(listener)

    def removeSubsListener(self, listener=None):
        self.dec.removeSubsListener(listener)


class SpeechPipeline(BasePipeline):
    def __init__(self, stream, runCb=None):
        ''' Speech recognition pipeline:

        Demux --> AudioDec --> Resampler --> SpeechRecognition --[words]--> {NgramSplitter} --[words]--> ...
        '''

        super().__init__(stream, runCb)

        speechModel = speech.loadSpeechModel(stream.lang)
        self.dec = gizmo.AudioDec()

        speechAudioFormat = speech.getSpeechAudioFormat(speechModel)
        logger.info('speech recognition audio format: %s', speechAudioFormat)

        self.speechRec = speech.createSpeechRec(speechModel)
        self.speechRec.setMinWordProb(settings().minWordProb)
        self.speechRec.setMinWordLen(settings().minWordLen)
        self.ngramSplitter = None
        self.sink = self.speechRec

        langInfo = stream.lang and languages.get(code3=stream.lang.lower())
        if langInfo and langInfo.ngrams:
            logger.info('switching to %i-gram for audio "%s"', langInfo.ngrams, stream.path)
            self.speechRec.setMinWordLen(langInfo.ngrams)
            self.ngramSplitter = gizmo.NgramSplitter(langInfo.ngrams)
            self.speechRec.addWordsListener(self.ngramSplitter.pushWord)
            self.sink = self.ngramSplitter

        self.resampler = gizmo.Resampler()
        self.channels = stream.channels
        self.resampler.connectFormatChangeCallback(self.onAudioFormatChanged)

        self.demux.connectDec(self.dec, stream.no)
        self.dec.connectOutput(self.resampler)
        self.resampler.connectOutput(self.speechRec, speechAudioFormat)

    def destroy(self):
        super().destroy()
        self.sink.removeWordsListener()
        self.speechRec.removeWordsListener()
        self.resampler.connectFormatChangeCallback(None)

    def onAudioFormatChanged(self, inFormat, outFormat):
        logger.info('input audio format: %s', inFormat)
        channelsMap = self.channels.getLayoutMap(inFormat.channelLayout)
        logger.info('listening to channels: %s', channelsMap)
        self.resampler.setChannelMap(channelsMap.getMap())

    def addWordsListener(self, listener):
        self.sink.addWordsListener(listener)

    def removeWordsListener(self, listener=None):
        return self.sink.removeWordsListener(listener)

    def getRawWordsSource(self):
        return self.speechRec


def createProducerPipeline(stream, runCb=None):
    if stream.type == 'subtitle/text':
        return SubtitlePipeline(stream, runCb)
    elif stream.type == 'audio':
        return SpeechPipeline(stream, runCb)
    else:
        raise Error(_('Not supported stream type'), type=stream.type)


def createProducerPipelines(stream, no=None, timeWindows=None, runCb=None):
    if timeWindows != None:
        no = len(timeWindows)

    pipes = []
    for i in range(no):

        p = createProducerPipeline(stream, runCb)
        pipes.append(p)

        if p.duration:
            if timeWindows != None:
                start, begin, end = timeWindows[i]

            else:
                partTime = p.duration / no
                begin = i * partTime
                end = begin + partTime
                start = None

            logger.info('job %i/%i time window set to %.2f - %.2f', i+1, no, begin, end)
            if start != None:
                logger.info('job %i/%i starting position set to %.2f', i+1, no, start)

            p.selectTimeWindow(begin, end, start)

        else:
            logger.warn('cannot get duration - using single pipeline')
            break

    return pipes
