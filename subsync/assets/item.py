from subsync.assets.downloader import Downloader
from subsync import config
from subsync import utils
from subsync.data import languages
from subsync.error import Error
import os
import json
import shutil
import subprocess
import stat

import logging
logger = logging.getLogger(__name__)


class Asset(object):
    def __init__(self, type, params):
        self.type = type
        self.params = params

        self._local = {}
        self._remote = {}
        self._updaterRunning = False

        fname = '{}.{}'.format('-'.join(params), type)
        self.path = os.path.join(config.assetdir, type, fname)
        self.localDir = None

    def getId(self):
        return mkId(self.type, self.params)

    def getPrettyName(self):
        return self.getId()

    def download(self, onUpdate=None, onEnd=None, timeout=None):
        if self._updaterRunning:
            raise RuntimeError(_('Asset downloader is already running'))

        downloader = Downloader()
        downloader.registerCallbacks(onUpdate=onUpdate, onEnd=onEnd)
        downloader.run(self, timeout=timeout)
        return downloader

    def isMissing(self):
        return bool(not self.localVersion() and not self.remoteVersion())

    def localVersion(self):
        if not self._local:
            try:
                self._local = self._readLocalData() or {}
            except Exception as e:
                logger.info('cannot load %s: %r', self.getPrettyName(), e)
                self._removeLocalData()
        return utils.parseVersion(self._local.get('version'))

    def remoteVersion(self):
        return utils.parseVersion(self._remote.get('version'))

    def hasUpdate(self):
        local = self.localVersion()
        remote = self.remoteVersion()
        return bool(local and remote and remote > local)

    def _removeLocalData(self):
        self._local = {}
        try:
            if self.path and os.path.isfile(self.path):
                logger.info('removing %s', self.path)
                os.remove(self.path)
        except:
            logger.error('cannot remove %s', self.getPrettyName(), exc_info=True)

        try:
            if self.localDir and os.path.isdir(self.localDir):
                logger.info('removing %s', self.localDir)
                shutil.rmtree(self.localDir, ignore_errors=True)
        except:
            logger.error('cannot remove %s', self.getPrettyName(), exc_info=True)

    def __repr__(self):
        return '<Asset {} local={} remote={}>'.format(
                self.getId(),
                self.localVersion(),
                self.remoteVersion())


class DictAsset(Asset):
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


class SpeechAsset(Asset):
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
        self.localVersion()
        return self._local


class SelfUpdaterAsset(Asset):
    def __init__(self, type, params):
        super().__init__(type, params)
        self.localDir = os.path.join(config.assetdir, 'upgrade')
        self.path = os.path.join(self.localDir, 'upgrade.json')
        self._updater = None

    def localVersion(self):
        return utils.getCurrentVersion()

    def installerVersion(self):
        return super().localVersion()

    def _readLocalData(self):
        if os.path.isfile(self.path):
            with open(self.path, encoding='utf8') as fp:
                return json.load(fp)

    def getPrettyName(self):
        return _('Application upgrade')

    def download(self, onUpdate=None, onEnd=None, timeout=None):
        upd = self._updater
        try:
            upd and not upd.isRunning() and upd.wait(reraise=True)
        except:
            upd = None

        if upd:
            upd.registerCallbacks(onUpdate=onUpdate, onEnd=onEnd)
        else:
            self._updater = upd = super().download(onUpdate, onEnd, timeout)
        return upd

    def hasInstaller(self):
        local = self.localVersion()
        installer = self.installerVersion()
        return bool(local and installer and installer > local)

    def install(self):
        try:
            self.installerVersion()
            instPath = os.path.join(self.localDir, self._local.get('install'))
            logger.info('executing installer %s', instPath)
            mode = os.stat(instPath).st_mode
            if (mode & stat.S_IEXEC) == 0:
                os.chmod(instPath, mode | stat.S_IEXEC)
            subprocess.Popen(instPath, cwd=self.localDir)

        except:
            logger.error('cannot install update %s', self.path, exc_info=True)
            self._removeLocalData()
            raise Error(_('Update instalation failed miserably'))


def getAssetTypeByName(typ, params=None):
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
