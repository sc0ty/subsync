from subsync import config
from subsync import pubkey
from subsync.error import Error
import os
import sys
import threading
import tempfile
import requests
import zipfile
import time

import logging
logger = logging.getLogger(__name__)


class Downloader(object):
    def __init__(self):
        self._onUpdate = set()
        self._onEnd = set()
        self._thread = None
        self._terminated = False
        self._exception = None
        self._lock = threading.Lock()

    def run(self, asset, timeout=None):
        if self._thread:
            raise RuntimeError('Another update in progress')

        self._terminated = False
        self._exception = None
        self._thread = threading.Thread(
                target=self._run,
                args=(asset, timeout),
                name="Download")
        self._thread.start()
        asset._updaterRunning = True

    def terminate(self):
        if self.isRunning():
            self._terminated = True

    def isRunning(self):
        return self._thread and self._thread.is_alive()

    def wait(self, reraise=False):
        self._thread and self._thread.join()
        if reraise and self._exception:
            _, ex, tb = self._exception
            raise ex.with_traceback(tb)
        return not self._terminated

    def registerCallbacks(self, onUpdate=None, onEnd=None):
        with self._lock:
            onUpdate and self._onUpdate.add(onUpdate)
            onEnd and self._onEnd.add(onEnd)

    def unregisterCallbacks(self, onUpdate=None, onEnd=None):
        with self._lock:
            onUpdate and self._onUpdate.remove(onUpdate)
            onEnd and self._onEnd.remove(onEnd)

    def _run(self, asset, timeout):
        try:
            with tempfile.TemporaryFile() as fp:
                hash = self._download(asset, fp, timeout)

                if not self._terminated:
                    try:
                        self._verify(asset, fp, hash)
                    except:
                        raise Error(_('Signature verification failed'),
                                asset=asset.getId(), url=asset._remote.get('url'))

                if not self._terminated:
                    try:
                        asset._removeLocalData()
                        self._install(asset, fp)
                    except Exception:
                        asset._removeLocalData()
                        raise Error(_('Asset installation failed'),
                                asset=asset.getId(), url=asset._remote.get('url'))

        except:
            e = sys.exc_info()
            self._exception = e
            logger.error('updater failed', exc_info=True)

        asset._updaterRunning = False
        with self._lock:
            for onEnd in self._onEnd:
                onEnd(asset, self._terminated, self._exception)

    def _download(self, asset, fp, timeout):
        logger.info('downloading asset %s', asset.getPrettyName())

        url = asset._remote['url']
        size = asset._remote.get('size')
        hash = pubkey.sha256()

        r = requests.get(url, stream=True, timeout=5)
        r.raise_for_status()
        size = int(r.headers.get('content-length', size))
        pos = 0

        if timeout is not None:
            lastTime = time.monotonic()

        def notifyUpdate():
            with self._lock:
                for onUpdate in self._onUpdate:
                    onUpdate(asset, pos, size)

        notifyUpdate()

        for chunk in r.iter_content(4096):
            fp.write(chunk)
            hash.update(chunk)
            pos += len(chunk)
            if self._terminated:
                return hash

            if timeout is not None:
                now = time.monotonic()
                if now - lastTime >= timeout:
                    lastTime = now
                    notifyUpdate()

        notifyUpdate()
        return hash

    def _verify(self, asset, fp, hash):
            logger.info('downloading signature')
            sig = asset._remote['sig']
            r = requests.get(sig, timeout=5)
            r.raise_for_status()
            signature = r.content
            if self._terminated:
                return

            logger.info('verifying signature')
            pubkey.verify(hash, signature)

    def _install(self, asset, fp):
        asset._local = None
        type = asset._remote['type']
        if type == 'zip':
            dstdir = config.assetdir
            logger.info('extracting zip asset to %s', dstdir)
            os.makedirs(dstdir, exist_ok=True)
            zipf = zipfile.ZipFile(fp)
            zipf.extractall(dstdir)
            logger.info('extraction completed')
            asset._local = None

        else:
            raise Error('Invalid asset type', asset=asset.getId(), type=type,
                    url=asset._remote.get('url'))
