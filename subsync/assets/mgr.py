from subsync.assets import item, listupdater, assetlist
from subsync import config, utils
import threading, json
import os

import logging
logger = logging.getLogger(__name__)


class AssetManager(object):
    """Manages remote and local assets.

    Assets are used for synchronization (speech recognition models,
    dictionaries) and application updates.
    Assets are available on remote server and could be installed locally.
    Single asset contains information for both local and remote part.
    Local part is not available if asset is not installed locally.
    Remote part is not available if there is no such asset on server or
    synchronization with server was not performed.
    """

    _instance = None

    def instance():
        """Get singleton instance of `AssetManager`."""
        if AssetManager._instance is None:
            AssetManager._instance = AssetManager()
        return AssetManager._instance

    def __init__(self):
        if AssetManager._instance is not None:
            return AssetManager._instance

        self._assets = {}
        self._listUpdater = None
        self._assetsLock = threading.RLock()

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
        """Get asset of given ID or type/params.

        Returned asset could have local and/or remote part set, or none if such
        asset don't exist.
        For given ID always the same object will be returned.
        """
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
                self._assets[id] = item.createAsset(typ, par)
            return self._assets[id]

    def getAssetsForTasks(self, tasks):
        """Get assets list for requested tasks.

        Parameters
        ----------
        tasks: iterable of subsync.synchro.SyncTask

        Returns
        -------
        subsync.assets.AssetList
        """
        assets = set()
        for task in tasks:
            sub, ref = task.sub, task.ref
            if ref and ref.type == 'audio':
                assets.add(self.getAsset('speech', [ref.lang]))
            if sub and sub.lang and ref and ref.lang and sub.lang != ref.lang:
                langs = sorted([sub.lang, ref.lang])
                assets.add(self.getAsset('dict', langs))
        return assetlist.AssetList(assets)

    def getAssetListUpdater(self, autoUpdate=False):
        """Get remote assets list updater.

        Parameters
        ----------
        autoUpdate: bool, optional
            When `True`, application upgrade will be downloaded automatically
            after list update (if upgrade is available).
            Setting `autoUpdate` has effect only on first call to this method.

        Returns
        -------
        subsync.assets.listupdater.ListUpdater
            Will return the same object for subsequent calls.
        """

        def onUpdate(assets):
            if assets:
                self._updateAssetsRemoteData(assets)
            if autoUpdate:
                self.runSelfUpdater()

        if not self._listUpdater:
            self._listUpdater = listupdater.ListUpdater(onUpdate=onUpdate)
        return self._listUpdater

    def runSelfUpdater(self):
        """Start self upgrade if available.

        Returns
        -------
        subsync.assets.downloader.AssetDownloader or None
            `None` if upgrade is not available.
        """
        asset = self.getSelfUpdaterAsset()
        if asset and asset.hasUpdate() and not asset.hasInstaller():
            logger.info('new version available to download, %s -> %s',
                    asset.localVersion(), asset.remoteVersion())
            downloader = asset.downloader()
            downloader and downloader.run(timeout=0.5)
            return downloader

    def isListUpToDate(self):
        """Check if asset list is synchronized with remote server."""
        return self._listUpdater and self._listUpdater.isUpdated()

    def getSelfUpdaterAsset(self):
        """Get asset corresponding with application upgrade (if exist)."""
        if config.assetupd and utils.getCurrentVersion():
            return self.getAsset(config.assetupd)

    def _updateAssetsRemoteData(self, assets):
        logger.info('updating remote asset list, got %i assets', len(assets))
        for id, remote in assets.items():
            if item.validateRemoteData(remote):
                asset = self.getAsset(id)
                self.getAsset(id)._setRemoteData(remote)
            else:
                logger.warning('invalid asset remote data: %r', remote)
                self.getAsset(id)._setRemoteData({})

        with self._assetsLock:
            for id in self._assets.keys() - assets.keys():
                logger.debug('asset %s removed from server', id)
                self.getAsset(id)._setRemoteData({})
