from subsync.assets.downloader import AssetDownloader
from subsync import config
from subsync import utils
from subsync.translations import _
from subsync.data import languages
from subsync.error import Error
import os
import json
import shutil
import threading
import subprocess
import stat

import logging
logger = logging.getLogger(__name__)

__pdoc__ = {
        'createAsset': False,
        'mkId': False,
        'parseId': False,
        'validateRemoteData': False,
        }


class Asset(object):
    """Single asset contains remote data from asset server and local
    installation data (if available, both parts could be empty).
    """

    def __init__(self, type, params):
        self.type = type
        self.params = params

        self._local = None
        self._remote = {}
        self._downloader = None
        self._lock = threading.RLock()

        fname = '{}.{}'.format('-'.join(params), type)
        self.path = os.path.join(config.assetdir, type, fname)
        self.localDir = None

    def getId(self):
        """Get asset identifier as `str`."""
        return mkId(self.type, self.params)

    def getPrettyName(self):
        """Get asset human-readable name."""
        return self.getId()

    def isMissing(self):
        """Check whether asset is unavailable.

        Returns
        -------
        bool
            `True` if asset is not available both locally and on server.
        """
        return bool(not self.localVersion() and not self.remoteVersion())

    def localVersion(self):
        """Get version of locally installed asset.

        Returns
        -------
        tuple of int or None
            Local version number or `None` if not installed locally.
        """
        return utils.parseVersion(self._getLocalData().get('version'))

    def remoteVersion(self):
        """Get version of asset available on server.

        Returns
        -------
        tuple of int or None
            Remote version number or `None` if not available on server.
        """
        return utils.parseVersion(self._remote.get('version'))

    def hasUpdate(self):
        """Check if remote version is available and is newer than local or asset
        is not installed locally.
        """
        local = self.localVersion()
        remote = self.remoteVersion()
        return bool(remote and (not local or remote > local))

    def downloader(self):
        """Get asset remote downloader.

        Returns
        -------
        subsync.assets.downloader.AssetDownloader or None
            If remote version exists and is newer than local (or asset is not
            installed locally) will return downloader, otherwise `None`.
            Returned downloader could be already running (e.g. for subsequent
            calls).
        """
        with self._lock:
            if self._downloader and self._downloader.isDone():
                self._downloader.unregisterAllCallbacks()
                self._downloader = None
            if not self._downloader and self.hasUpdate():
                self._downloader = AssetDownloader(self)
            return self._downloader

    def _getLocalData(self):
        with self._lock:
            if self._local is None:
                try:
                    self._local = self._readLocalData() or {}
                except Exception as e:
                    logger.info('cannot load %s: %r', self.getId(), e)
                    self._removeLocalData()
            return self._local

    def _removeLocalData(self):
        with self._lock:
            self._local = {}
            try:
                if self.path and os.path.isfile(self.path):
                    logger.info('removing %s', self.path)
                    os.remove(self.path)
            except:
                logger.error('cannot remove %s', self.getId(), exc_info=True)

            try:
                if self.localDir and os.path.isdir(self.localDir):
                    logger.info('removing %s', self.localDir)
                    shutil.rmtree(self.localDir, ignore_errors=True)
            except:
                logger.error('cannot remove %s', self.getId(), exc_info=True)

    def _setRemoteData(self, remote):
        with self._lock:
            self._remote = remote

    def _getRemoteData(self):
        with self._lock:
            return self._remote

    def __repr__(self):
        return '<Asset {} local={} remote={}>'.format(
                self.getId(),
                self._getLocalData().get('version'),
                self._remote.get('version'))


class DictAsset(Asset):
    """Dictionary asset."""

    def _readLocalData(self):
        with open(self.path, encoding='utf8') as fp:
            ents = fp.readline().strip().split('/', 3)

        if len(ents) >= 4 and ents[0] == '#dictionary':
            return { 'lang1': ents[1], 'lang2': ents[2], 'version': ents[3] }
        else:
            return { 'version': '0.0.0' }

    def getPrettyName(self):
        return _('dictionary {} / {}').format(
                languages.getName(self.params[0]),
                languages.getName(self.params[1]))

    def readDictionary(self):
        try:
            logger.info('reading dictionary from file "%s"', self.path)
            with open(self.path, 'r', encoding='utf8') as fp:
                for line in fp:
                    line = line.strip()
                    if not line or line[0] == '#':
                        continue
                    ents = line.split('|')
                    if len(ents) >= 2:
                        for val in ents[1:]:
                            yield (ents[0], val)
                    else:
                        logger.warning("invalid dictionary entry '%s'", line)
        except:
            self._removeLocalData()
            raise


class SpeechAsset(Asset):
    """Speech recognition model asset."""

    def _readLocalData(self):
        with open(self.path, encoding='utf8') as fp:
            local = json.load(fp)

        if 'version' not in local:
            local['version'] = '0.0.0'

        # fix local paths
        dirname = os.path.abspath(os.path.dirname(self.path))
        sphinx = local.get('sphinx', None)
        if sphinx:
            for key, val in sphinx.items():
                if val.startswith('./'):
                    sphinx[key] = os.path.join(dirname, *val.split('/')[1:])

        localDir = local.get('dir', None)
        if localDir and localDir.startswith('./'):
            localDir = os.path.join(dirname, *localDir.split('/')[1:])

        self.localDir = localDir
        return local

    def getPrettyName(self):
        return _('{} speech recognition model').format(
                languages.getName(self.params[0]))

    def readSpeechModel(self):
        return self._getLocalData()


class SelfUpdaterAsset(Asset):
    """Application upgrade asset."""

    def __init__(self, type, params):
        super().__init__(type, params)
        self.localDir = os.path.join(config.assetdir, 'upgrade')
        self.path = os.path.join(self.localDir, 'upgrade.json')

    def localVersion(self):
        """Same as application version."""
        return utils.getCurrentVersion()

    def installerVersion(self):
        """Get version of locally downloaded installer.

        Returns
        -------
        tuple of int
            Installer version if installer is downloaded and ready to be run,
            `None` otherwise.
        """
        return super().localVersion()

    def _readLocalData(self):
        if os.path.isfile(self.path):
            with open(self.path, encoding='utf8') as fp:
                return json.load(fp)

    def getPrettyName(self):
        return _('Application upgrade')

    def hasInstaller(self):
        """Check if installer is downloaded and could be run."""
        local = self.localVersion()
        installer = self.installerVersion()
        return bool(local and installer and installer > local)

    def install(self):
        """Run local installer.

        Application must be terminated immediately to let installer work.
        """
        with self._lock:
            try:
                self.installerVersion()
                instPath = os.path.join(self.localDir, self._getLocalData().get('install'))
                logger.info('executing installer %s', instPath)
                mode = os.stat(instPath).st_mode
                if (mode & stat.S_IEXEC) == 0:
                    os.chmod(instPath, mode | stat.S_IEXEC)
                subprocess.Popen(instPath, cwd=self.localDir)

            except:
                logger.error('cannot install update %s', self.path, exc_info=True)
                self._removeLocalData()
                raise Error(_('Update instalation failed miserably'))


def createAsset(typ, params=None):
    types = {
            'dict':    DictAsset,
            'speech':  SpeechAsset,
            'subsync': SelfUpdaterAsset,
            }

    T = types.get(typ, Asset)
    return T(typ, params)


def mkId(type, params):
    return '{}/{}'.format(type, '-'.join(params))


def parseId(id):
    ents = id.split('/', 1)
    if len(ents) == 2:
        return ents[0], ents[1].split('-')
    elif len(ents) == 1:
        return ents[0], None
    else:
        return None, None


def validateRemoteData(data):
    if data.get('type') not in [ 'zip' ]:
        return False
    if not isinstance(data.get('url'), str):
        return False
    if not isinstance(data.get('sig'), str):
        return False
    if not utils.parseVersion(data.get('version')):
        return False
    return True
