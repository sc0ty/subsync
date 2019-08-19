import gizmo
from subsync import assets
from subsync.data import languages
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


def loadDictionary(lang1, lang2, minLen=0):
    dictionary = gizmo.Dictionary()

    reverse1 = lang1 in languages.languagesRTL
    reverse2 = lang2 in languages.languagesRTL

    asset = assets.getAsset('dict', (lang1, lang2))
    if asset.isLocal():
        for key, val in loadDictionaryFromFile(asset.path):
            if len(key) >= minLen and len(val) >= minLen:
                if reverse1: key = key[::-1]
                if reverse2: val = val[::-1]
                dictionary.add(key, val)

    else:
        asset = assets.getAsset('dict', (lang2, lang1))
        if asset.isLocal():
            for key, val in loadDictionaryFromFile(asset.path):
                if len(key) >= minLen and len(val) >= minLen:
                    if reverse1: val = val[::-1]
                    if reverse2: key = key[::-1]
                    dictionary.add(val, key)

    if not asset.isLocal():
        raise Error(_('There is no dictionary for transaltion from {} to {}')
                    .format(lang1, lang2)) \
                    .add('language1', lang1) \
                    .add('language2', lang2)

    logger.info('dictionary ready with %u entries', dictionary.size())
    return dictionary


def loadDictionaryFromFile(path):
    logger.info('loading dictionary: "%s"', path)
    with open(path, 'r', encoding='utf8') as fp:
        for line in fp:
            if len(line) > 0 and line[0] != '#':
                ents = line.strip().split('|')
                if len(ents) >= 2:
                    key = ents[0].lower()
                    for val in ents[1:]:
                        yield (key, val.lower())
