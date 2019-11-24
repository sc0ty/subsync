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
import hashlib
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)


UpdaterStatus = namedtuple('UpdaterStatus', [
    'state',
    'detail',
    'progress',
    'error'
])


class Updater(thread.AsyncJob):
    def __init__(self, asset):
        self.asset = asset

        self.lock = threading.Lock()
        self.state = 'idle'
        self.detail = None
        self.progress = None
        self.error = None

        super().__init__(self.job, name='Download')

        for key in ['type', 'url', 'sig']:
            if key not in asset.getRemote():
                raise Error('Invalid asset data, missing parameter', key=key)

    def start(self):
        self.setStatus(state='run')
        super().start()

    def setStatus(self, state=None, detail=None, progress=None, error=None):
        with self.lock:
            if state is not None:
                self.state = state
                self.detail = detail
            if progress is not None:
                self.progress = progress
            if error is not None:
                self.error = error

    def getStatus(self):
        with self.lock:
            return UpdaterStatus(
                    state=self.state,
                    detail=self.detail,
                    progress=self.progress,
                    error=self.error)

    async def job(self):
        logger.info('downloading asset %s', self.asset.getPrettyName())
        installing = False
        try:
            with tempfile.TemporaryFile() as fp:
                self.setStatus(state='run', detail='download')
                fp, hash = await self.download(fp)
                self.setStatus(state='run', detail='install')
                await self.verify(hash)
                self.asset.removeLocal()
                installing = True
                await self.install(fp)
                self.asset.updateLocal()
                installing = False
                self.setStatus(state='done', detail='success')

        except asyncio.CancelledError:
            logger.info('operation cancelled by user')
            if installing:
                self.asset.removeLocal()
            self.setStatus(state='done', detail='cancel')

        except Exception as e:
            logger.error('download failed, %r', e, exc_info=True)
            if installing:
                self.asset.removeLocal()
            self.setStatus(state='done', detail='fail', error=sys.exc_info())

    async def download(self, fp):
        url = self.asset.getRemote('url')
        size = self.asset.getRemote('size')

        logger.info('downloading %s', url)
        hash = pubkey.sha256()

        def onNewChunk(chunk, progress):
            self.setStatus(progress=progress)
            hash.update(chunk)

        await async_utils.downloadFileProgress(url, fp, size, chunkCb=onNewChunk)
        return fp, hash

    async def verify(self, hash):
        logger.info('downloading signature')
        sig = await async_utils.downloadRaw(self.asset.getRemote('sig'))

        logger.info('verifying signature')
        try:
            pubkey.verify(hash, sig)
        except:
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
