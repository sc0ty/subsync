import gizmo
from subsync.synchro import speech
from subsync.data import languages
from subsync.error import Error
import math

import logging
logger = logging.getLogger(__name__)


class BasePipeline(object):
    def __init__(self, stream, runCb=None):
        self.demux = gizmo.Demux(stream.path, runCb)
        self.extractor = gizmo.Extractor(self.demux)

        self.duration = max(self.demux.getDuration(), 0)
        self.timeWindow = [0, self.duration]

    def destroy(self):
        self.extractor.stop()
        self.extractor.wait()
        self.extractor.connectEosCallback(None)
        self.extractor.connectErrorCallback(None)

    def selectTimeWindow(self, begin, end=math.inf):
        if begin != 0.0:
            self.demux.seek(begin)
        if end is not math.inf:
            self.extractor.selectEndTime(end)
        else:
            end = self.duration
        self.timeWindow = (begin, end)

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
        self.extractor.connectEosCallback(cb)


class SubtitlePipeline(BasePipeline):
    def __init__(self, stream, runCb=None):
        ''' Speech recognition pipeline:

        Demux --> SpeechDec --[words]--> {NgramSplitter} --[words]--> ...
        '''

        super().__init__(stream, runCb)
        self.dec = gizmo.SubtitleDec()
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

    def configure(self, minWordLen, minWordProb=None):
        self.dec.setMinWordLen(minWordLen)

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

    def configure(self, minWordLen, minWordProb):
        self.speechRec.setMinWordProb(minWordProb)
        self.speechRec.setMinWordLen(minWordLen)

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


def createProducerPipelines(stream, no=None, runCb=None):
    pipes = []
    for i in range(no):
        p = createProducerPipeline(stream, runCb)
        pipes.append(p)

        if p.duration:
            if p.duration / (i+1) < 5*60:
                logger.info('using only %i jobs due to short duration', i+1)
                break
        else:
            logger.warn('cannot get duration - using single pipeline')
            break

    if len(pipes) > 1:
        no = len(pipes)
        duration = pipes[0].duration
        partTime = duration / no
        for i, p in enumerate(pipes):
            begin = i * partTime
            end = begin + partTime + 1.0 # overlap to catch whole words
            if end >= duration:
                end = math.inf
            logger.info('job %i/%i time window set to %.2f - %.2f', i+1, no, begin, end)

            try:
                p.selectTimeWindow(begin, end)
            except gizmo.Error:
                logger.warning('seek failed, using only %i jobs', i, exc_info=True)
                no = i
                pipes = pipes[:no]
                if pipes:
                    logger.info('updating job %i/%i time window set to %.2f - %.2f',
                            no, no, begin - partTime, duration)
                    pipes[-1].selectTimeWindow(begin - partTime, duration)
                break

    return pipes
