from subsync import config
from subsync import utils
from subsync.assets import local
from subsync.assets import remote
from subsync.assets.downloader import AssetDownloader
from subsync.assets.updater import SelfUpdater

remoteAssets = None


def init(updateCb):
    global remoteAssets
    remoteAssets = remote.RemoteAssets(updateCb)

def terminate():
    global remoteAssets
    if remoteAssets:
        remoteAssets.terminate()
        remoteAssets = None

def getLocalAsset(*args, **kwargs):
    return local.getAsset(*args, **kwargs)

def getRemoteAsset(*args, **kwargs):
    return remoteAssets.getAsset(*args, **kwargs)

def isUpdateAvailable():
    if config.assetupd:
        currentVer = utils.getCurrentVersion()
        remoteUpdate = getRemoteAsset(**config.assetupd)
        remoteVer = utils.parseVersion(remoteUpdate.get('version'))
        return currentVer and remoteVer and currentVer < remoteVer

def getAssetPrettyName(type, params, **kw):
    if type == 'speech':
        return _('{} speech recognition model').format(
                utils.getLanguageName(params[0]))
    elif type == 'dict':
        return _('dictionary {} / {}').format(
                utils.getLanguageName(params[0]),
                utils.getLanguageName(params[1]))
    else:
        return '{}/{}'.format(type, '-'.join(params))

