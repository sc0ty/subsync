import gizmo
from assets import assets
from error import Error
import os

import logging
logger = logging.getLogger(__name__)


def loadDictionary(lang1, lang2, minLen=0):
    dictionary = gizmo.Dictionary()

    dictPath = assets.getLocalAsset('dict', (lang1, lang2))
    if dictPath:
        for key, val in loadDictionaryFromFile(dictPath):
            if len(key) >= minLen and len(val) >= minLen:
                dictionary.add(key, val)

    else:
        dictPath = assets.getLocalAsset('dict', (lang2, lang1))
        if dictPath:
            for key, val in loadDictionaryFromFile(dictPath):
                if len(key) >= minLen and len(val) >= minLen:
                    dictionary.add(val, key)

    if not dictPath:
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
