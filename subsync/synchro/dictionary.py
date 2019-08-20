import gizmo
from subsync import assets
from subsync.data import languages
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


def loadDictionary(langKey, langVal, minLen=0):
    langKeyInfo = languages.get(code3=langKey)
    langValInfo = languages.get(code3=langVal)

    dictionary = gizmo.Dictionary(
            minLen=minLen,
            rightToLeftKey=langKeyInfo.rightToLeft,
            rightToLeftVal=langValInfo.rightToLeft,
            ngramsKey=langKeyInfo.ngrams or 0,
            ngramsVal=langValInfo.ngrams or 0);

    asset = assets.getAsset('dict', (langKey, langVal))
    if asset.isLocal():
        for key, val in loadDictionaryFromFile(asset.path):
            dictionary.add(key, val)
    else:
        asset = assets.getAsset('dict', (langVal, langKey))
        if asset.isLocal():
            for key, val in loadDictionaryFromFile(asset.path):
                dictionary.add(val, key)

    if not asset.isLocal():
        raise Error(_('There is no dictionary for transaltion from {} to {}')
                    .format(langKey, langVal)) \
                    .add('language1', langKey) \
                    .add('language2', langVal)

    logger.info('dictionary ready with %u entries', dictionary.size())
    return dictionary


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
