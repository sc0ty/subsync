import gizmo
from assets import assets
import utils
import error
import json
import os

import logging
logger = logging.getLogger(__name__)


audio_channel_center_id = 2

_speechModels = {}

def loadSpeechModel(lang):
    if lang in _speechModels:
        return _speechModels[lang]

    logger.info('loading speech recognition model for language %s', lang)

    path = assets.getLocalAsset('speech', [lang], raiseIfMissing=True)
    with open(path, encoding='utf8') as fp:
        model = json.load(fp)

    # fix paths
    if 'sphinx' in model:
        dirname = os.path.abspath(os.path.dirname(path))
        sphinx = model['sphinx']
        for key, val in sphinx.items():
            if val.startswith('./'):
                sphinx[key] = os.path.join(dirname, *val.split('/')[1:])

    logger.debug('model ready: %s', model)
    _speechModels[lang] = model
    return model


def createSpeechRec(model):
    speechRec = gizmo.SpeechRecognition()
    if 'sphinx' in model:
        for key, val in model['sphinx'].items():
            speechRec.setParam(key, val)
    return speechRec


def getSpeechAudioFormat(speechModel, inputAudioFormat):
    try:
        sampleFormat = getattr(gizmo.AVSampleFormat,
                speechModel.get('sampleformat', 'S16'))

        sampleRate = speechModel.get('samplerate', 16000)
        if type(sampleRate) == str:
            sampleRate = int(sampleRate)

        channelLayout = 1
        if inputAudioFormat.channelLayout:
            channelId = utils.onesPositions(inputAudioFormat.channelLayout)[0]
            channelLayout = 1 << channelId

        return gizmo.AudioFormat(sampleFormat, sampleRate, channelLayout)
    except:
        raise error.Error(_('Invalid speech audio format'),
                inputFormat=str(inputAudioFormat))


def getDefaultAudioChannels(audio):
    ''' Center channel will be selected if available,
    otherwise all channels will be mixed together
    '''

    channels = utils.onesPositions(audio.channelLayout)
    if audio_channel_center_id in channels:
        return [ audio_channel_center_id ]

    return channels


class MixMap:
    def __init__(self, channelsNo = 0):
        self.channelsNo = channelsNo
        self.map = [ 0.0 ] * channelsNo * channelsNo

    def setPath(self, srcNo, dstNo, gain = 1.0):
        self.map[srcNo + dstNo*self.channelsNo] = gain

    def mixAll(self, dstNo, gain = 1.0):
        g = gain / self.channelsNo
        for srcNo in range(self.channelsNo):
            self.setPath(srcNo, dstNo, g)

    def __repr__(self):
        if self.channelsNo == 0:
            return '<MixMap map=none>'
        if self.map == [ 0.0 ] * len(self.map):
            return '<MixMap map=zero>'

        items = []
        no = self.channelsNo
        for dst, srcs in enumerate([ self.map[ x*no : (x+1)*no ] for x in range(no) ]):
            if srcs == [ 0.0 ] * no:
                items.append('[0]=>{}'.format(dst))
            else:
                items.append('{}=>{}'.format(srcs, dst))
        return '<MixMap {}>'.format(', '.join(items))

