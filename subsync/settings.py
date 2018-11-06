import config
import os
import json
from error import Error

import logging
logger = logging.getLogger(__name__)


class Settings(object):
    def __init__(self, settings=None, **kw):
        self.language = None
        self.maxPointDist = 2.0
        self.minPointsNo = 20
        self.appendLangCode = True
        self.windowSize = 30.0 * 60.0
        self.minWordProb = 0.3
        self.jobsNo = None
        self.minWordLen = 5
        self.minCorrelation = 0.9999
        self.minWordsSim = 0.6
        self.lastdir = ''
        self.autoUpdate = True
        self.askForUpdate = True
        self.debugOptions = False
        self.logLevel = logging.WARNING
        self.logFile = None
        self.logBlacklist = None

        if settings:
            self.set(**settings.items())
        self.set(**kw)

    def __eq__(self, other):
        for key in self.__dict__.keys() | other.__dict__.keys():
            if not hasattr(self, key) or not hasattr(other, key):
                return False
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    def set(self, **state):
        for key, val in state.items():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                logger.warning('invalid entry: %s = %s (%s)',
                        key, str(val), type(val).__name__)

    def items(self):
        return {k: v for k, v in self.__dict__.items()}

    def load(self):
        try:
            if os.path.isfile(config.configpath):
                with open(config.configpath, encoding='utf8') as fp:
                    cfg = json.load(fp)
                    logger.info('configuration loaded from %s', config.configpath)
                    logger.debug('configuration: %r', cfg)
                    self.set(**cfg)
        except Exception as err:
            raise Error(_('Cannot load settings file, {}').format(err), path=config.configpath)

    def save(self):
        try:
            os.makedirs(os.path.dirname(config.configpath), exist_ok=True)
            with open(config.configpath, 'w', encoding='utf8') as fp:
                json.dump(self.items(), fp, indent=4)
            logger.info('configuration saved to %s', config.configpath)
            logger.debug('configuration: %r', self.items())
        except Exception as e:
            logger.warning('cannot save configuration to %s: %r', config.configpaths, e)


_settings = Settings()


def settings():
    return _settings

