import assets
import assets.updater
import config
import utils
import error
import json
import asyncio
import aiohttp
import threading
import itertools
import os

import logging
logger = logging.getLogger(__name__)


class RemoteAssets(object):
    def __init__(self, updateCb):
        self.assets = {}
        self.assetsLock = threading.Lock()

        self.loop = None
        self.task = None

        def runUpdate():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.task = asyncio.ensure_future(self.updateJob(updateCb))
            self.loop.run_until_complete(self.task)
            self.loop.close()

        self.thread = threading.Thread(target=runUpdate)
        if config.assetsurl:
            self.thread.start()

    def terminate(self):
        if self.thread.isAlive():
            self.loop.call_soon_threadsafe(self.task.cancel)
            self.thread.join()

    def getAsset(self, type, params, permutable=False, raiseIfMissing=False):
        if permutable:
            paramsPerm = itertools.permutations(params)
        else:
            paramsPerm = [ params ]

        for params in paramsPerm:
            assetId = '{}/{}'.format(type, '-'.join(params))
            with self.assetsLock:
                if assetId in self.assets:
                    asset = self.assets[assetId]
                    asset['title'] = assets.getAssetPrettyName(type, params)
                    return asset

        if raiseIfMissing:
            raise error.Error(_('Missing {}').format(
                assets.getAssetPrettyName(type, params)),
                type=type, params=params)

    async def updateJob(self, updateCb):
        try:
            await self.loadList()
            await self.downloadAssets()

            localUpdate = assets.updater.getLocalUpdate()
            if localUpdate:
                localVer = localUpdate['version']
                currentVer = utils.getCurrentVersion()
                logger.info('update version: %s, current version: %s',
                        localVer, currentVer)

                if currentVer == None or currentVer >= localVer:
                    assets.updater.removeLocalUpdate()

            if updateCb:
                updateCb()

        except asyncio.CancelledError:
            pass

    async def downloadAssets(self):
        try:
            logger.info('downloading assets list from %s', config.assetsurl)
            async with aiohttp.ClientSession() as session:
                async with session.get(config.assetsurl) as response:
                    assert response.status == 200
                    res = await response.json(content_type=None)

            logger.info('got %i assets', len(res))

            with self.assetsLock:
                self.assets = res

            await self.saveList()

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('asset list download failed, %r', e, exc_info=True)

    async def loadList(self):
        try:
            if os.path.isfile(config.assetspath):
                with open(config.assetspath, encoding='utf8') as fp:
                    assets = json.load(fp)

                with self.assetsLock:
                    self.assets = assets

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('cannot load assets list from %s: %r',
                    config.assetspath, e, exc_info=True)

    async def saveList(self):
        try:
            with open(config.assetspath, 'w', encoding='utf8') as fp:
                json.dump(self.assets, fp, indent=4)

        except asyncio.CancelledError:
            raise

        except Exception as e:
            logger.error('cannot write assets list to %s: %r',
                    config.assetspath, e, exc_info=True)

