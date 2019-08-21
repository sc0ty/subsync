import gizmo
from subsync import assets
from subsync.data import languages
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
                    dictionary.add(key.lower(), val)

    asset = assets.getAsset('dict', (langKey, langVal))
    if asset.isLocal():
        for key, val in loadDictionaryFromFile(asset.path):
            addEntry(key, val)
    else:
        asset = assets.getAsset('dict', (langVal, langKey))
        if asset.isLocal():
            for key, val in loadDictionaryFromFile(asset.path):
                addEntry(val, key)

    if not asset.isLocal():
        raise Error(_('There is no dictionary for transaltion from {} to {}')
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


def loadDictionaryFromFile(path):
    logger.info('loading dictionary: "%s"', path)
    with open(path, 'r', encoding='utf8') as fp:
        for line in fp:
            if len(line) > 0 and line[0] != '#':
                ents = line.strip().split('|')
                if len(ents) >= 2:
                    key = ents[0]
                    for val in ents[1:]:
                        yield (key, val)
