from subsync import config
from subsync import utils
from subsync import thread
from subsync import async_utils
import asyncio
import sys

import logging
logger = logging.getLogger(__name__)


class AssetListUpdater(thread.AsyncJob):
    def __init__(self, mgr):
        super().__init__(self.updateJob, name='AssetListUpdater')
        self.mgr = mgr

    async def updateJob(self, updateList=True, autoUpdate=False, onError=None):
        await self.loadRemoteAssetList()
        if updateList:
            await self.downloadRemoteAssetList(onError)
        self.removeOldInstaller()
        if autoUpdate:
            await self.runAutoUpdater(onError)

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

    async def downloadRemoteAssetList(self, onError):
        try:
            if config.assetsurl:
                logger.info('downloading remote assets list from %s', config.assetsurl)
                assets = await async_utils.downloadJson(config.assetsurl)
                if assets:
                    await async_utils.writeJsonFile(config.assetspath, assets)
                    self.updateRemoteAssetsData(assets)

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('cannot download asset list from %s: %r', config.assetsurl, e)
            if onError:
                onError(sys.exc_info())

    async def runAutoUpdater(self, onError):
        try:
            updAsset = self.mgr.getSelfUpdaterAsset()
            updater = updAsset and updAsset.getUpdater()
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

                    updater.start()

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('update processing failed: %r', e, exc_info=True)
            if onError:
                onError(sys.exc_info())

    def removeOldInstaller(self):
        cur = utils.getCurrentVersion()
        if cur:
            updAsset = self.mgr.getSelfUpdaterAsset()
            if updAsset:
                loc = updAsset.localVersion(None)
                rem = updAsset.remoteVersion(None)
                if loc and loc <= cur:
                    updAsset.removeLocal()
                elif loc and rem and loc < rem:
                    updAsset.removeLocal()

    def updateRemoteAssetsData(self, remoteData):
        logger.info('update remote asset list, got %i assets', len(remoteData))
        for id, remote in remoteData.items():
            self.mgr.getAsset(id).updateRemote(remote)
