from subsync.assets import item
from subsync import config
from subsync import utils
from subsync import thread
from subsync import async_utils
from subsync.settings import settings
import threading
import asyncio

import logging
logger = logging.getLogger(__name__)


class AssetManager(object):
    def __init__(self):
        self.assets = {}
        self.lock = threading.Lock()
        self.updateTask = thread.AsyncJob(self.updateJob, name='AssetsUpdater')
        self.remoteAssetListReady = False

        self.removeOldInstaller()

    async def updateJob(self):
        await self.loadRemoteAssetList()
        await self.downloadRemoteAssetList()
        self.removeOldInstaller()
        await self.runAutoUpdater()

    async def loadRemoteAssetList(self):
        try:
            logger.info('reading remote asset list from %s', config.assetspath)
            assets = await async_utils.readJsonFile(config.assetspath)
            if assets:
                self.updateRemoteAssetsData(assets)

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('cannot read asset list from %s: %r',
                    config.assetspath, e, exc_info=True)

    async def downloadRemoteAssetList(self):
        try:
            if config.assetsurl:
                logger.info('downloading remote assets list from %s', config.assetsurl)
                assets = await async_utils.downloadJson(config.assetsurl)
                if assets:
                    await async_utils.writeJsonFile(config.assetspath, assets)
                    self.updateRemoteAssetsData(assets)
                    self.remoteAssetListReady = True

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('cannot download asset list from %s: %r', config.assetsurl, e)

    async def runAutoUpdater(self):
        try:
            updAsset = self.getSelfUpdaterAsset()
            updater = updAsset.getUpdater() if updAsset else None
            cur = utils.getCurrentVersion()

            if updater and cur:
                loc = updAsset.localVersion(None)
                rem = updAsset.remoteVersion(None)

                if (loc and cur >= loc) or (loc and rem and rem > loc):
                    updAsset.removeLocal()
                    loc = None

                if rem and not loc and rem > cur:
                    logger.info('new version available to download, %s -> %s',
                            utils.versionToString(cur),
                            utils.versionToString(rem))

                    if settings().autoUpdate:
                        updater.start()

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('update processing failed: %r', e, exc_info=True)

    def removeOldInstaller(self):
        cur = utils.getCurrentVersion()
        if cur:
            updAsset = self.getSelfUpdaterAsset()
            if updAsset:
                loc = updAsset.localVersion(None)
                rem = updAsset.remoteVersion(None)
                if loc and loc <= cur:
                    updAsset.removeLocal()
                elif loc and rem and loc < rem:
                    updAsset.removeLocal()

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

    def getSelfUpdaterAsset(self):
        if config.assetupd:
            return self.getAsset(config.assetupd)

    def updateRemoteAssetsData(self, remoteData):
        logger.info('update remote asset list, got %i assets', len(remoteData))
        for id, remote in remoteData.items():
            self.getAsset(id).updateRemote(remote)

