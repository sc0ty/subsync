import locale
from data.languages import languages, languages2to3
from error import Error

import logging
logger = logging.getLogger(__name__)


def detectEncoding(path, lang, probeSize=32*1024):
    dlang, denc = locale.getdefaultlocale()
    if not lang:
        lang2 = dlang.split('_', 1)[0]
        lang = languages2to3.get(lang2)

    encs = [ 'UTF-8' ] + languages.get(lang, (None, []))[1]
    if denc not in encs:
        encs.append(denc)

    try:
        for enc in encs:
            with open(path, 'r', encoding=enc) as fp:
                try:
                    fp.read(32 * 1024)
                    logger.info('detected encoding %s for file "%s"', enc, path)
                    return enc
                except UnicodeError:
                    pass
    except FileNotFoundError:
        raise Error('File not found').add('path', path)

    logger.info('couldn\'t detect encoding for file "%s", tried %s', path, encs)

