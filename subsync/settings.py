from subsync import config
from subsync.error import Error
import os
import json

import logging
logger = logging.getLogger(__name__)


persistent = {
        'language': None,
        'maxPointDist': 2.0,
        'minPointsNo': 20,
        'appendLangCode': True,
        'outputCharEnc': 'UTF-8',
        'windowSize': 30.0 * 60.0,
        'minWordProb': 0.3,
        'jobsNo': None,
        'minWordLen': 5,
        'minCorrelation': 0.9999,
        'minWordsSim': 0.6,
        'minEffort': 0.5,
        'lastdir': '',
        'refsCache': True,
        'autoUpdate': True,
        'askForUpdate': True,
        'showLanguageNotSelectedPopup': True,
        'showBatchDropTargetPopup': True,
        'batchSortFiles': False,
        'debugOptions': False,
        'logLevel': logging.WARNING,
        'logFile': None,
        'logBlacklist': None,
        }


volatile = {
        'cli': False,
        'mode': None,
        'tasks': None,
        'verbose': 1,
        'exitWhenDone': False,
        'dumpSubWords': None,
        'dumpRefWords': None,
        'dumpRawSubWords': None,
        'dumpRawRefWords': None,
        'dumpUsedSubWords': None,
        'dumpUsedRefWords': None,
        }


class Settings(object):
    def __init__(self, settings=None, **kw):
        self.keep = {}

        for key, val in persistent.items():
            setattr(self, key, val)
            self.keep[key] = val

        for key, val in volatile.items():
            setattr(self, key, val)

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

    def set(self, temp=False, **state):
        for key, val in state.items():
            if hasattr(self, key):
                setattr(self, key, val)
                if not temp and key in persistent:
                    self.keep[key] = val
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
                json.dump(self.keep, fp, indent=4)
            logger.info('configuration saved to %s', config.configpath)
            logger.debug('configuration: %r', items)
        except Exception as e:
            logger.warning('cannot save configuration to %s: %r', config.configpath, e)


_settings = Settings()


def settings():
    return _settings

