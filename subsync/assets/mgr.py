from subsync.assets import item, listupdater
from subsync import config, utils
import threading, json
import os

import logging
logger = logging.getLogger(__name__)


class AssetManager(object):
    def __init__(self):
        self._assets = {}
        self._listUpdater = None
        self._assetsLock = threading.Lock()

        try:
            if os.path.isfile(config.assetspath):
                logger.info('reading remote asset list from %s', config.assetspath)
                with open(config.assetspath, encoding='utf8') as fp:
                    self._updateAssetsRemoteData(json.load(fp))
        except:
            logger.error('cannot read asset list from %s',
                    config.assetspath, exc_info=True)

        updAsset = self.getSelfUpdaterAsset()
        if updAsset:
            local = updAsset.localVersion()
            installer = updAsset.installerVersion()
            if local and installer and local >= installer:
                logger.info('removing old installer (%s) files', installer)
                updAsset._removeLocalData()

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

        with self._assetsLock:
            if id not in self._assets:
                self._assets[id] = item.getAssetTypeByName(typ, par)
            return self._assets[id]

    def getAssetsForTasks(self, tasks):
        assets = set()
        for task in tasks:
            sub, ref = task.sub, task.ref
            if ref and ref.type == 'audio':
                assets.add(self.getAsset('speech', [ref.lang]))
            if sub and sub.lang and ref and ref.lang and sub.lang != ref.lang:
                langs = sorted([sub.lang, ref.lang])
                assets.add(self.getAsset('dict', langs))
        return AssetList(assets)

    def getAssetListUpdater(self, autoUpdate=False):

        def onUpdate(assets):
            if assets:
                self._updateAssetsRemoteData(assets)
            if autoUpdate:
                self.runSelfUpdater()

        if not self._listUpdater:
            self._listUpdater = listupdater.ListUpdater(onUpdate=onUpdate)
        return self._listUpdater

    def runSelfUpdater(self):
        asset = self.getSelfUpdaterAsset()
        if asset and asset.hasUpdate() and not asset.hasInstaller():
            logger.info('new version available to download, %s -> %s',
                    asset.localVersion(), asset.remoteVersion())
            return asset.download(timeout=0.5)

    def isListUpToDate(self):
        return self._listUpdater and not self._listUpdater.isRunning()

    def getSelfUpdaterAsset(self):
        if config.assetupd and utils.getCurrentVersion():
            return self.getAsset(config.assetupd)

    def _updateAssetsRemoteData(self, assets):
        logger.info('updating remote asset list, got %i assets', len(assets))
        for id, remote in assets.items():
            if item.validateRemoteData(remote):
                self.getAsset(id)._remote = remote
            else:
                logger.warning('invalid asset remote data: %r', remote)
                self.getAsset(id)._remote = {}

        with self._assetsLock:
            for id in self._assets.keys() - assets.keys():
                logger.debug('asset %s removed from server', id)
                self._assets[id]._remote = {}


class AssetList(object):
    def __init__(self, assets):
        self._assets = assets

    def __len__(self):
        return len(self._assets)

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        return self._assets.__iter__()

    def __getitem__(self, pos):
        return self._assets[pos]

    def __repr__(self):
        return '[{}]'.format(', '.join([ repr(a) for a in self._assets ]))

    def missing(self):
        return AssetList([ a for a in self._assets if a.isMissing() ])

    def hasUpdate(self):
        return AssetList([ a for a in self._assets if a.hasUpdate() ])

    def installed(self):
        return AssetList([ a for a in self._assets if a.localVersion() ])

    def notInstalled(self):
        return AssetList([ a for a in self._assets if not a.localVersion() ])
