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
        'lastSubLang': None,
        'lastRefLang': None,
        'refsCache': True,
        'autoUpdate': True,
        'askForUpdate': True,
        'showLanguageNotSelectedPopup': True,
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
        'dumpWords': [],
        }


outdated = [
        'showBatchDropTargetPopup',
        ]


wordsDumpIds = [ 'sub', 'subPipe', 'subRaw', 'ref', 'refPipe', 'refRaw' ]


class Settings(object):
    def __init__(self, settings=None, **kw):
        self.keep = {}
        self.dirty = False

        self.persistent = persistent.keys()
        self.volatile = volatile.keys()

        for key, val in persistent.items():
            setattr(self, key, val)
            self.keep[key] = val

        for key, val in volatile.items():
            setattr(self, key, val)

        if settings:
            self.set(**{ k: settings.get(k) for k in settings.keys() })
        self.set(**kw)

    def __eq__(self, other):
        for key in self.keys() | other.keys():
            if not hasattr(self, key) or not hasattr(other, key):
                return False
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    def keys(self, persistentOnly=False, volatileOnly=False):
        if persistentOnly:
            return self.persistent
        elif volatileOnly:
            return self.volatile
        else:
            return self.persistent | self.volatile

    def set(self, temp=False, **state):
        dirty = self.dirty
        for key, val in state.items():
            dirty = self.setValue(key, val, temp=temp) or dirty
        self.dirty = dirty
        return dirty

    def setValue(self, key, val, temp=False):
        if key in persistent or key in volatile:
            logger.debug('updating entry: %s = %s', key, str(val))
            setattr(self, key, val)
            if not temp and key in persistent and self.keep[key] != val:
                self.keep[key] = val
                return True
        elif key in outdated:
            logger.warning('outdated entry: %s = %s, dropping', key, str(val))
        else:
            logger.warning('invalid entry: %s = %s (%s)', key, str(val), type(val).__name__)
        return False

    def get(self, key):
        if key in self.keys():
            return getattr(self, key)

    def getAll(self):
        return { key: self.get(key) for key in self.keys() }

    def load(self):
        try:
            if os.path.isfile(config.configpath):
                with open(config.configpath, encoding='utf8') as fp:
                    cfg = json.load(fp)
                    logger.info('configuration loaded from %s', config.configpath)
                    logger.debug('configuration: %r', cfg)

                    dirty = self.dirty
                    self.set(temp=False, **{ **persistent, **cfg })
                    self.dirty = dirty
        except Exception as err:
            raise Error(_('Cannot load settings file, {}').format(err), path=config.configpath)

    def save(self):
        if self.dirty:
            try:
                os.makedirs(os.path.dirname(config.configpath), exist_ok=True)
                with open(config.configpath, 'w', encoding='utf8') as fp:
                    json.dump(self.keep, fp, indent=4)
                self.dirty = False
                logger.info('configuration saved to %s', config.configpath)
                logger.debug('configuration: %r', self.keep)
            except Exception as e:
                logger.warning('cannot save configuration to %s: %r', config.configpath, e)

_settings = Settings()


def settings():
    return _settings

