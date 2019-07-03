from subsync.assets import item
from subsync import config
import threading

import logging
logger = logging.getLogger(__name__)


class AssetManager(object):
    def __init__(self):
        self.assets = {}
        self.lock = threading.Lock()
        self.assetListUpdater = None

    def getAsset(self, assetId, params=None):
        if params:
            typ = assetId
            par = params
            id = item.mkId(typ, par)
        elif isinstance(assetId, str):
            id = assetId
            typ, par = item.parseId(assetId)
        else:
            typ = assetId[0]
            par = assetId[1]
            id = item.mkId(typ, par)

        with self.lock:
            if id not in self.assets:
                self.assets[id] = item.getAssetTypeByName(typ, par)
            return self.assets[id]

    def getAssetsForTask(self, task):
        res = set()
        if task.ref.type == 'audio':
            res.add(self.getAsset('speech', [task.ref.lang]))
        if task.sub.lang and task.ref.lang and task.sub.lang != task.ref.lang:
            langs = sorted([task.sub.lang, task.ref.lang])
            res.add(self.getAsset('dict', langs))
        return res

    def getSelfUpdaterAsset(self):
        if config.assetupd:
            return self.getAsset(config.assetupd)
