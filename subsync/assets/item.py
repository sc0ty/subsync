from subsync.assets.updater import Updater
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

        self.local = None
        self.remote = None
        self.updater = None

        fname = '{}.{}'.format('-'.join(params), type)
        self.path = os.path.join(config.assetdir, type, fname)
        self.localDir = None

    def updateLocal(self):
        self.local = {}

    def updateRemote(self, remote):
        self.remote = remote

    def getPrettyName(self):
        return mkId(self.type, self.params)

    def getLocal(self, key=None, defaultValue=None):
        if self.local == None:
            self.updateLocal()
        local = self.local or {}
        if key:
            return local.get(key, defaultValue)
        else:
            return local

    def getRemote(self, key=None, defaultValue=None):
        remote = self.remote or {}
        if key:
            return remote.get(key, defaultValue)
        else:
            return remote

    def getUpdater(self):
        if not self.updater and self.remote:
            self.updater = Updater(self)
        return self.updater

    def isLocal(self):
        return bool(self.getLocal())

    def isRemote(self):
        return bool(self.getRemote())

    def isMissing(self):
        return not self.isLocal() and not self.isRemote()

    def localVersion(self, defaultVersion=(0, 0, 0)):
        return utils.parseVersion(self.getLocal('version'), defaultVersion)

    def remoteVersion(self, defaultVersion=(0, 0, 0)):
        return utils.parseVersion(self.getRemote('version'), defaultVersion)

    def isUpgradable(self):
        return self.remoteVersion() > self.localVersion()

    def validateLocal(self):
        pass

    def removeLocal(self):
        try:
            if self.path and os.path.isfile(self.path):
                logger.info('removing %s', self.path)
                os.remove(self.path)
        except Exception as e:
            logger.error('cannot remove %s: %r', self.getPrettyName(), e, exc_info=True)

        try:
            if self.localDir and os.path.isdir(self.localDir):
                logger.info('removing %s', self.localDir)
                shutil.rmtree(self.localDir, ignore_errors=True)
        except Exception as e:
            logger.error('cannot remove %s: %r', self.getPrettyName(), e, exc_info=True)

        self.local = {}

    def isUpgradable(self):
        return self.isRemote() and self.remoteVersion() > self.localVersion()

    def __repr__(self):
        return '<Asset {} local={} remote={} path={}>'.format(
                mkId(self.type, self.params),
                self.getLocal(),
                self.isRemote(),
                self.path)


class DictAsset(Asset):
    def updateLocal(self):
        try:
            with open(self.path, encoding='utf8') as fp:
                ents = fp.readline().strip().split('/', 3)

            if len(ents) >= 4 and ents[0] == '#dictionary':
                self.local = dict(
                        lang1 = ents[1],
                        lang2 = ents[2],
                        version = ents[3])

        except Exception as e:
            logger.warn('cannot load %s: %r', self.getPrettyName(), e)
            self.removeLocal()

    def getPrettyName(self):
        if len(self.params) >= 2:
            return _('dictionary {} / {}').format(
                    languages.getName(self.params[0]),
                    languages.getName(self.params[1]))
        else:
            super().getPrettyName()


class SpeechAsset(Asset):
    def updateLocal(self):
        try:
            with open(self.path, encoding='utf8') as fp:
                local = json.load(fp)

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

            self.local = local
            self.localDir = localDir

        except Exception as e:
            logger.warn('cannot load %s: %r', self.getPrettyName(), e)
            self.removeLocal()

    def getPrettyName(self):
        if len(self.params) >= 1:
            return _('{} speech recognition model').format(
                    languages.getName(self.params[0]))
        else:
            super().getPrettyName()


class UpdateAsset(Asset):
    def __init__(self, type, params):
        super().__init__(type, params)
        self.localDir = os.path.join(config.assetdir, 'upgrade')
        self.path = os.path.join(self.localDir, 'upgrade.json')

    def updateLocal(self):
        try:
            if os.path.isfile(self.path):
                with open(self.path, encoding='utf8') as fp:
                    self.local = json.load(fp)

        except Exception as e:
            logger.warn('cannot load %s: %r', self.getPrettyName(), e)
            self.removeLocal()

    def installUpdate(self):
        try:
            instPath = os.path.join(self.localDir, self.getLocal('install'))
            logger.info('executing installer %s', instPath)
            mode = os.stat(instPath).st_mode
            if (mode & stat.S_IEXEC) == 0:
                os.chmod(instPath, mode | stat.S_IEXEC)
            subprocess.Popen(instPath, cwd=self.localDir)

        except Exception as e:
            logger.error('cannot install update %s: %r', self.path, e, exc_info=True)
            self.removeLocal()
            raise Error(_('Update instalation failed miserably'))

    def hasUpdate(self):
        return self.hasRemoteUpdate() or self.hasLocalUpdate()

    def hasLocalUpdate(self):
        cur = utils.getCurrentVersion()
        return cur and self.isLocal() and self.localVersion() > cur

    def hasRemoteUpdate(self):
        cur = utils.getCurrentVersion()
        return cur and self.isRemote() and self.remoteVersion() > cur


def getAssetTypeByName(typ, params=None):
    types = {
            'dict':    DictAsset,
            'speech':  SpeechAsset,
            'subsync': UpdateAsset,
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

