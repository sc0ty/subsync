import gizmo
from subsync import speech
from subsync import utils
from subsync.settings import settings
from subsync.error import Error
import math

import logging
logger = logging.getLogger(__name__)


class BasePipeline(object):
    def __init__(self, stream):
        self.demux = gizmo.Demux(stream.path)
        self.extractor = gizmo.Extractor(self.demux)

        self.duration = self.demux.getDuration()
        self.timeWindow = [0, self.duration]

    def destroy(self):
        self.extractor.connectEosCallback(None)
        self.extractor.connectErrorCallback(None)
        self.extractor.stop()

    def selectTimeWindow(self, *window):
        self.timeWindow = window
        self.extractor.selectTimeWindow(*window)

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
            return (pos - self.timeWindow[0]) / (self.timeWindow[1] - self.timeWindow[0])

    def connectEosCallback(self, cb, dst=None):
        self.extractor.connectEosCallback(cb)

    def connectErrorCallback(self, cb, dst=None):
        self.extractor.connectErrorCallback(cb)


class SubtitlePipeline(BasePipeline):
    def __init__(self, stream):
        ''' Speech recognition pipeline:

        Demux --> SpeechDec  --[words]--> ...
        '''

        super().__init__(stream)
        self.dec = gizmo.SubtitleDec()
        self.dec.setMinWordLen(settings().minWordLen)
        if stream.enc != None:
            self.dec.setEncoding(stream.enc)

        self.demux.connectDec(self.dec, stream.no)

    def destroy(self):
        super().destroy()
        self.dec.connectWordsCallback(None)
        self.dec.connectSubsCallback(None)

    def connectWordsCallback(self, cb):
        self.dec.connectWordsCallback(cb)

    def connectSubsCallback(self, cb):
        self.dec.connectSubsCallback(cb)


class SpeechPipeline(BasePipeline):
    def __init__(self, stream):
        ''' Speech recognition pipeline:

        Demux --> AudioDec --> Resampler --> SpeechRecognition --[words]--> ...
        '''

        super().__init__(stream)

        speechModel = speech.loadSpeechModel(stream.lang)
        self.dec = gizmo.AudioDec()

        speechAudioFormat = speech.getSpeechAudioFormat(speechModel)
        logger.info('speech recognition audio format: %s', speechAudioFormat)

        self.speechRec = speech.createSpeechRec(speechModel)
        self.speechRec.setMinWordProb(settings().minWordProb)
        self.speechRec.setMinWordLen(settings().minWordLen)

        self.resampler = gizmo.Resampler()
        self.channels = stream.channels
        self.resampler.connectFormatChangeCallback(self.onAudioFormatChanged)

        self.demux.connectDec(self.dec, stream.no)
        self.dec.connectOutput(self.resampler)
        self.resampler.connectOutput(self.speechRec, speechAudioFormat)

    def destroy(self):
        super().destroy()
        self.speechRec.connectWordsCallback(None)
        self.resampler.connectFormatChangeCallback(None)

    def onAudioFormatChanged(self, inFormat, outFormat):
        logger.info('input audio format: %s', inFormat)
        channelsMap = self.channels.getLayoutMap(inFormat.channelLayout)
        logger.info('listening to channels: %s', channelsMap)
        self.resampler.setChannelMap(channelsMap.getMap())

    def connectWordsCallback(self, cb):
        self.speechRec.connectWordsCallback(cb)


def createProducerPipeline(stream):
    if stream.type == 'subtitle/text':
        return SubtitlePipeline(stream)
    elif stream.type == 'audio':
        return SpeechPipeline(stream)
    else:
        raise Error(_('Not supported stream type'), type=stream.type)


def createProducerPipelines(stream, no):
    pipes = []
    for i in range(no):
        p = createProducerPipeline(stream)
        pipes.append(p)

        if p.duration:
            partTime = p.duration / no
            begin = i * partTime
            end = begin + partTime
            logger.info('job %i/%i time window set to %.2f - %.2f', i+1, no, begin, end)
            p.selectTimeWindow(begin, end)

        else:
            logger.warn('cannot get duration - using single pipeline')
            break

    return pipes

