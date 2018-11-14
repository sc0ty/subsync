import gettext
import locale
import os
import config

import logging
logger = logging.getLogger(__name__)


def init():
    gettext.install('messages', localedir=config.localedir)

def setLanguage(lang):
    try:
        if lang == None:
            lang = locale.getdefaultlocale()[0].split('_', 1)[0]

        logger.info('changing translation language to %s', lang)

        if lang == 'en':
            gettext.install('messages', localedir=config.localedir)

        else:
            tr = gettext.translation('messages',
                    localedir=config.localedir,
                    languages=[lang])
            tr.install()

    except Exception as e:
        logger.warning('translation language setup failed, %r', e, exc_info=True)

def listLanguages():
    try:
        langs = os.listdir(config.localedir)
    except:
        langs = []

    if 'en' not in langs:
        langs.append('en')

    return langs
