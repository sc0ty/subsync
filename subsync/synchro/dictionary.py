import gizmo
from subsync import assets
from subsync.data import languages
from subsync.translations import _
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


def loadDictionary(langKey, langVal, minLen=0):
    langKeyInfo = languages.get(code3=langKey)
    langValInfo = languages.get(code3=langVal)

    minKeyLen = langKeyInfo.ngrams or minLen
    minValLen = langValInfo.ngrams or minLen

    dictionary = gizmo.Dictionary()

    def addEntry(key, val):
        if len(key) >= minKeyLen and len(val) >= minValLen:
            if langKeyInfo.rightToLeft: key = key[::-1]
            if langValInfo.rightToLeft: val = val[::-1]
            for k in splitNgrams(key, langKeyInfo.ngrams):
                for v in splitNgrams(val, langValInfo.ngrams):
                    dictionary.add(k.lower(), v)

    asset = assets.getAsset('dict', (langKey, langVal))
    if asset.localVersion():
        for key, val in asset.readDictionary():
            addEntry(key, val)
    else:
        asset = assets.getAsset('dict', (langVal, langKey))
        if asset.localVersion():
            for key, val in asset.readDictionary():
                addEntry(val, key)

    if not asset.localVersion():
        raise Error(_('There is no dictionary for transaltion from {} to {}') \
                .format(langKey, langVal)) \
                .add('language1', langKey) \
                .add('language2', langVal)

    logger.info('dictionary ready with %u entries', dictionary.size())
    return dictionary


def splitNgrams(word, size):
    if size:
        for i in range(len(word) + 1 - size):
            yield word[i:i+size]
    else:
        yield word
