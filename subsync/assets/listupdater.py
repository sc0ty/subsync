from subsync import config
from subsync.translations import _
import threading, requests, json
import sys

import logging
logger = logging.getLogger(__name__)


class ListUpdater(object):
    """Update assets list from remote server.

    Don't instantiate it manually, use
    `subsync.assets.mgr.AssetManager.getAssetListUpdater`.
    """

    def __init__(self, onUpdate=None):
        self._thread = None
        self._updated = False
        self._exception = None
        self._onUpdate = onUpdate

    def run(self):
        """Start updater (asynchronously)."""
        if self.isRunning():
            raise RuntimeError(_('Another update in progress'))

        self._exception = None
        self._updated = False
        self._thread = threading.Thread(
                target=self._run,
                name='AssetListUpdater')
        self._thread.start()

    def isUpdated(self):
        """Check if update was run and succeeded."""
        return self._updated

    def isRunning(self):
        """Check if update is running."""
        return self._thread and self._thread.is_alive()

    def wait(self, reraise=False):
        """Wait for update to finish.

        Blocks until update finishes, if running.

        Parameters
        ----------
        reraise: bool, optional
            If set, eventual exception from update thread will be raised here.
        """
        if self._thread:
            self._thread.join()
            if reraise and self._exception:
                _, ex, tb = self._exception
                raise ex.with_traceback(tb)

    def _run(self):
        try:
            logger.info('downloading remote asset list from %s', config.assetsurl)
            r = requests.get(config.assetsurl, timeout=5)
            r.raise_for_status()
            assets = r.json()
            self._onUpdate and self._onUpdate(assets)
            self._updated = True

            try:
                with open(config.assetspath, 'w', encoding='utf8') as fp:
                    json.dump(assets, fp, indent=4)
            except:
                    logger.info('cannot save asset list to %s',
                            config.assetspath, exc_info=True)

        except:
            logger.error('cannot download asset list from %s',
                    config.assetsurl, exc_info=True)
            self._exception = sys.exc_info()

