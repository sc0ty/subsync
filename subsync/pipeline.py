import gizmo
import speech
from settings import settings
from error import Error
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

    def start(self):
        self.extractor.start()

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
        self.dec = gizmo.SubtitleDec(self.demux, stream.no)
        self.dec.setMinWordLen(settings().minWordLen)
        if stream.enc != None:
            self.dec.setEncoding(stream.enc)

        self.demux.connectDec(self.dec, stream.no)

    def destroy(self):
        super().destroy()
        self.dec.connectWordsCallback(None, None)
        self.dec.connectSubsCallback(None, None)

    def connectWordsCallback(self, cb, dst=None):
        self.dec.connectWordsCallback(cb, dst)

    def connectSubsCallback(self, cb, dst=None):
        self.dec.connectSubsCallback(cb, dst)


class SpeechPipeline(BasePipeline):
    def __init__(self, stream):
        ''' Speech recognition pipeline:

        Demux --> AudioDec --[inputAudioFormat]--> AudioResampler -->
        --> AudioDemux --[speechAudioFormat]--> SpeechRecognition --[words]--> ...
        '''

        super().__init__(stream)

        speechModel = speech.loadSpeechModel(stream.lang)
        self.dec = gizmo.AudioDec(self.demux, stream.no)

        inputAudioFormat = self.dec.getFormat()
        speechAudioFormat = speech.getSpeechAudioFormat(speechModel, inputAudioFormat)
        logger.info('audio format conversion %r to %r', inputAudioFormat, speechAudioFormat)

        self.speechRec = speech.createSpeechRec(speechModel)
        self.speechRec.setMinWordProb(settings().minWordProb)
        self.speechRec.setMinWordLen(settings().minWordLen)

        self.audioDemux = gizmo.AudioDemux()
        self.audioDemux.setOutputFormat(speechAudioFormat.getSampleSize(),
                speechAudioFormat.channelsNo)

        if inputAudioFormat.channelsNo > 1:
            mixMap = speech.MixMap(inputAudioFormat.channelsNo)
            centerNo = speech.MixMap.getChannelNoByName('front center', inputAudioFormat)
            if centerNo != None:
                mixMap.setPath(centerNo, 0)
            else:
                mixMap.mixAll(0)
        else:
            mixMap = speech.MixMap()

        logger.debug('audio channels mixer map %r', mixMap)
        self.resampler = gizmo.AudioResampler()
        self.resampler.setParams(inputAudioFormat, speechAudioFormat, mixMap.map)

        self.demux.connectDec(self.dec, stream.no)
        self.dec.connectOutput(self.resampler)
        self.resampler.connectOutput(self.audioDemux)
        self.audioDemux.connectOutputChannel(0, self.speechRec)

    def destroy(self):
        super().destroy()
        self.speechRec.connectWordsCallback(None, None)

    def connectWordsCallback(self, cb, dst=None):
        self.speechRec.connectWordsCallback(cb, dst)


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

