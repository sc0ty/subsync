import gizmo
from subsync import assets
from subsync import error

import logging
logger = logging.getLogger(__name__)


def loadSpeechModel(lang):
    logger.info('loading speech recognition model for language %s', lang)

    asset = assets.getAsset('speech', [lang])
    if asset.isLocal():
        logger.debug('model ready: %s', asset.getLocal())
        return asset.getLocal()

    raise error.Error(_('There is no speech recognition model for language {}')
            .format(lang)).add('language', lang)


def createSpeechRec(model):
    speechRec = gizmo.SpeechRecognition()
    if 'sphinx' in model:
        for key, val in model['sphinx'].items():
            speechRec.setParam(key, val)
    return speechRec


def getSpeechAudioFormat(speechModel):
    try:
        sampleFormat = getattr(gizmo.AVSampleFormat,
                speechModel.get('sampleformat', 'S16'))

        sampleRate = speechModel.get('samplerate', 16000)
        if type(sampleRate) == str:
            sampleRate = int(sampleRate)

        return gizmo.AudioFormat(sampleFormat, sampleRate, 1)
    except:
        raise error.Error(_('Invalid speech audio format'))
