import config
import thread
import utils
from error import Error
import requests
import json
import threading
import time
import itertools
import os

import logging
logger = logging.getLogger(__name__)


class Assets(object):
    def __init__(self):
        self.assets = {}
        self.lock = threading.Lock()
        self.updateThread = thread.Thread(
                target=self.updateJob, done=self.onFinish, error=self.onFinish)
        self.onFinish = None
        self.loadList()

    def getLocalAsset(self, type, params, permutable=False, raiseIfMissing=False):
        if permutable:
            paramsPerm = itertools.permutations(params)
        else:
            paramsPerm = [ params ]

        for params in paramsPerm:
            fname = '{}.{}'.format('-'.join(params), type)
            path = os.path.join(config.assetdir, type, fname)
            if os.path.isfile(path):
                return path

        if raiseIfMissing:
            raise Error(_('Missing {}').format(getAssetPrettyName(type, params)),
                    type=type, params=params)

    def getRemoteAsset(self, type, params, permutable=False, raiseIfMissing=False):
        if permutable:
            paramsPerm = itertools.permutations(params)
        else:
            paramsPerm = [ params ]

        for params in paramsPerm:
            assetId = '{}/{}'.format(type, '-'.join(params))
            with self.lock:
                if assetId in self.assets:
                    asset = self.assets[assetId]
                    asset['title'] = getAssetPrettyName(type, params)
                    return asset

        if raiseIfMissing:
            raise Error(_('Missing {}').format(getAssetPrettyName(type, params)),
                    type=type, params=params)

    def update(self, delay=None, onFinish=None):
        self.onFinish = onFinish
        self.updateThread.start(name='Assets', daemon=True, kwargs={'delay':delay})

    def updateJob(self, delay=None):
        if delay:
            time.sleep(delay)

        try:
            assets = requests.get(config.assetsurl).json()
            with self.lock:
                self.assets = assets
        except Exception as e:
            logger.error('cannto get assets list from %s: %r', config.assetsurl, e)

        yield
        with self.lock:
            self.saveList()

    def onFinish(self, err=None):
        with self.lock:
            onFinish = self.onFinish
        if onFinish:
            onFinish(err)

    def loadList(self):
        try:
            if os.path.isfile(config.assetspath):
                with open(config.assetspath, encoding='utf8') as fp:
                    assets = json.load(fp)
                self.assets = assets
        except Exception as e:
            logger.error('cannot load assets list from %s: %r', config.assetspath, e)

    def saveList(self):
        try:
            with open(config.assetspath, 'w', encoding='utf8') as fp:
                json.dump(self.assets, fp, indent=4)
        except Exception as e:
            logger.error('cannot write assets list to %s: %r', config.assetspath, e)


def getAssetPrettyName(type, params, **kw):
    if type == 'speech':
        return _('{} speech recognition model').format(
                utils.getLanguageName(params[0]))
    elif type == 'dict':
        return _('dictionary {} / {}').format(
                utils.getLanguageName(params[0]),
                utils.getLanguageName(params[1]))
    else:
        return '{}/{}'.format(type, '-'.join(params))

