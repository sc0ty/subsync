from subsync import config
from subsync import pubkey
from subsync.translations import _
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


class AssetDownloader(object):
    """Downloads and installs remote assets from server locally.

    Don't instantiate it manually, use `subsync.assets.item.Asset.downloader`
    instead.
    """
    def __init__(self, asset):
        self._asset = asset
        self._onUpdate = set()
        self._onEnd = set()
        self._thread = None
        self._terminated = False
        self._exception = None
        self._lock = threading.RLock()

    def run(self, timeout=None):
        """Start downloader (asynchronously).

        Could be called multiple times, has no effect if downloader is already
        in progress.  If downloader is already running, timeout will not be
        updated. See `AssetDownloade.registerCallbacks`.

        Parameters
        ----------
        timeout: float, optional
            How often `onUpdate` callback should be called (in seconds).

        Returns
        -------
        bool
            `True` if new update was started, `False` if update is already in
            progress.
        """
        if self._thread:
            return False

        if not self._asset.hasUpdate():
            raise RuntimeError('No update available')

        self._terminated = False
        self._exception = None
        self._thread = threading.Thread(
                target=self._run,
                args=(timeout,),
                name="Download")
        self._thread.start()
        return True

    def terminate(self):
        """Stop downloader if running."""
        if self.isRunning():
            self._terminated = True

    def isRunning(self):
        """Check whether downloader is running.

        It is running if it was started and not yet finished (either
        successfully or not) and was not terminated.
        """
        return self._thread and self._thread.is_alive()

    def isDone(self):
        """Check if downloader is done.

        It is done when it was started and finished (either successfully or
        not) or was terminated.
        """
        return self._thread and not self._thread.is_alive()

    def wait(self, reraise=False):
        """Wait for downloader to finish.

        Blocks until downloader finishes. If reraise is `True`, eventual
        exception from downloader thread will be raised here.

        Returns
        -------
        bool
            `True` if downloader finished itself (either successfully or not),
            `False` in case it was terminated.
        """
        self._thread and self._thread.join()
        if reraise and self._exception:
            _, ex, tb = self._exception
            raise ex.with_traceback(tb)
        return not self._terminated

    def registerCallbacks(self, listener=None, *, onUpdate=None, onEnd=None):
        """Register status callbacks.

        Peridoically during download `onUpdate`(asset, progress, size) is
        called, with asset set to `subsync.assets.item.Asset` object, progress
        and size contains downloaded bytes and total size. Size could be `None`
        if not known. If timeout (set in `AssetDownloader.run`) is `None` -
        `onUpdate` will not be called.

        At finish `onEnd`(asset, terminated, exception) is called, with
        terminated set to `True` in case if download was terminated and
        exception set to eventual exception raised in downloader thread, `None`
        otherwise.  Callback registered when updater is done
        (`AssetDownloader.isDone` returns `True`) will be called immediately
        from the caller thread (before this method returns).

        Callbacks could be also specified as listener object with methods named
        as arguments above. None callbacks are required. Explicit callbacks
        takes precedence over listener object methods.
        """
        onUpdate = onUpdate or getattr(listener, 'onUpdate', None)
        onEnd = onEnd or getattr(listener, 'onEnd', None)
        with self._lock:
            if self.isDone():
                onEnd and onEnd(self._asset, self._terminated, self._exception)
            else:
                onUpdate and self._onUpdate.add(onUpdate)
                onEnd and self._onEnd.add(onEnd)

    def unregisterCallbacks(self, listener=None, onUpdate=None, onEnd=None):
        """Unregister callbacks registered by
        `AssetDownloader.registerCallbacks`.
        """
        onUpdate = onUpdate or getattr(listener, 'onUpdate', None)
        onEnd = onEnd or getattr(listener, 'onEnd', None)
        with self._lock:
            onUpdate and self._onUpdate.discard(onUpdate)
            onEnd and self._onEnd.discard(onEnd)

    def unregisterAllCallbacks(self):
        """Unregister all status callbacks."""
        with self._lock:
            self._onUpdate.clear()
            self._onEnd.clear()

    def _run(self, timeout):
        try:
            remote = self._asset._getRemoteData()
            url = remote.get('url')

            for key in [ 'url', 'sig', 'type' ]:
                if not isinstance(remote.get(key), str):
                    logger.warning('invalid asset remote data %r', remote)
                    return

            with tempfile.TemporaryFile() as fp:
                hash = self._download(fp, url, remote.get('size'), timeout)

                if not self._terminated:
                    try:
                        self._verify(fp, remote.get('sig'), hash)
                    except:
                        raise Error(_('Signature verification failed'),
                                asset=self._asset.getId(), url=url)

                if not self._terminated:
                    try:
                        self._asset._removeLocalData()
                        self._install(fp, remote.get('type'))
                    except Exception:
                        self._asset._removeLocalData()
                        raise Error(_('Asset installation failed'),
                                asset=self._asset.getId(), url=url)

        except:
            e = sys.exc_info()
            self._exception = e
            logger.error('updater failed', exc_info=True)

        finally:
            with self._lock:
                for onEnd in self._onEnd:
                    onEnd(self._asset, self._terminated, self._exception)

    def _download(self, fp, url, size, timeout):
        logger.info('downloading asset %s', self._asset.getId())

        hash = pubkey.sha256()

        r = requests.get(url, stream=True, timeout=5)
        r.raise_for_status()
        try:
            size = int(r.headers.get('content-length', size))
        except:
            size = None
        pos = 0

        if timeout is not None:
            lastTime = time.monotonic()
            self._notifyUpdate(pos, size)

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
                    self._notifyUpdate(pos, size)

        if timeout is not None:
            self._notifyUpdate(pos, size)

        return hash

    def _notifyUpdate(self, pos, size):
        with self._lock:
            for onUpdate in self._onUpdate:
                onUpdate(self._asset, pos, size)

    def _verify(self, fp, sig, hash):
            logger.info('downloading signature')
            r = requests.get(sig, timeout=5)
            r.raise_for_status()
            signature = r.content
            if self._terminated:
                return

            logger.info('verifying signature')
            pubkey.verify(hash, signature)

    def _install(self, fp, type):
        with self._asset._lock:
            self._asset._local = None
            if type == 'zip':
                dstdir = config.assetdir
                logger.info('extracting zip asset to %s', dstdir)
                os.makedirs(dstdir, exist_ok=True)
                zipf = zipfile.ZipFile(fp)
                zipf.extractall(dstdir)
                logger.info('extraction completed')

            else:
                raise Error('Invalid asset type', asset=self._asset.getId(), type=type,
                        url=self._asset._getRemoteData().get('url'))
