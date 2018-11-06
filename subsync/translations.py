import gettext
import locale
import os
import config

import logging
logger = logging.getLogger(__name__)


_localedir = None

def init():
    global _localedir
    for d in config.localedirs:
        if os.path.isdir(d):
            logger.info('using translations from %s', d)
            _localedir = d
            break

    gettext.install('messages', localedir=_localedir)

def setLanguage(lang):
    try:
        if lang == None:
            lang = locale.getdefaultlocale()[0].split('_', 1)[0]

        logger.info('changing translation language to %s', lang)

        if lang == 'en':
            gettext.install('messages', localedir=_localedir)

        else:
            tr = gettext.translation('messages',
                    localedir=_localedir,
                    languages=[lang])
            tr.install()

    except Exception as e:
        logger.warning('translation language setup failed, %r', e, exc_info=True)

def listLanguages():
    if _localedir:
        langs = os.listdir(_localedir)
    else:
        langs = []

    if 'en' not in langs:
        langs.append('en')

    return langs
