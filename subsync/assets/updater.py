from subsync import config
from subsync import thread
from subsync import pubkey
from subsync import async_utils
from subsync.error import Error
import os
import sys
import threading
import asyncio
import tempfile
import zipfile
import Crypto

import logging
logger = logging.getLogger(__name__)


class Updater(thread.AsyncJob):
    def __init__(self, asset):
        self.asset = asset

        self.lock = threading.Lock()
        self.done = False
        self.progress = 0
        self.error = None

        super().__init__(self.job, name='Download')

        for key in ['type', 'url', 'sig']:
            if key not in asset.getRemote():
                raise Error('Invalid asset data, missing parameter', key=key)

    def start(self):
        self.setState(done=False, progress=0.0, error=None)
        super().start()

    def setState(self, **kw):
        with self.lock:
            for key, value in kw.items():
                setattr(self, key, value)

    def getState(self):
        with self.lock:
            return self.done, self.progress, self.error

    async def job(self):
        logger.info('downloading asset %s', self.asset.getPrettyName())
        try:
            with tempfile.TemporaryFile() as fp:
                fp, hash = await self.download(fp)
                self.setState(progress=1.0)
                await self.verify(hash)
                self.asset.removeLocal()
                await self.install(fp)
                self.asset.updateLocal()

        except asyncio.CancelledError:
            logger.info('operation cancelled by user')
            self.asset.removeLocal()
            self.setState(result=False)

        except Exception as e:
            logger.error('download failed, %r', e, exc_info=True)
            self.asset.removeLocal()
            self.setState(error=sys.exc_info())

        finally:
            self.setState(done=True)

    async def download(self, fp):
        url = self.asset.getRemote('url')
        size = self.asset.getRemote('size')

        logger.info('downloading %s', url)
        hash = Crypto.Hash.SHA256.new()

        def onNewChunk(chunk, progress):
            self.setState(progress=progress)
            hash.update(chunk)

        await async_utils.downloadFileProgress(url, fp, size, chunkCb=onNewChunk)
        return fp, hash

    async def verify(self, hash):
        logger.info('downloading signature')
        sig = await async_utils.downloadRaw(self.asset.getRemote('sig'))

        logger.info('verifying signature')
        if not pubkey.getVerifier().verify(hash, sig):
            raise Error(_('Signature verification failed'),
                    url=self.asset.getRemote('url'))

        logger.info('signature is valid')

    async def install(self, fp):
        assetType = self.asset.getRemote('type')
        if assetType == 'zip':
            dstdir = config.assetdir
            logger.info('extracting zip asset to %s', dstdir)
            os.makedirs(dstdir, exist_ok=True)
            zipf = zipfile.ZipFile(fp)
            zipf.extractall(dstdir)
            logger.info('extraction completed')

        else:
            raise Error('Invalid asset type',
                    type=assetType,
                    url=self.asset.getRemote('url'))

