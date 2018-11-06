import config
import utils
import assets.local
import assets.remote

remoteAssets = None


def init(updateCb):
    global remoteAssets
    remoteAssets = assets.remote.RemoteAssets(updateCb)

def terminate():
    global remoteAssets
    if remoteAssets:
        remoteAssets.terminate()
        remoteAssets = None

def getLocalAsset(*args, **kwargs):
    return assets.local.getAsset(*args, **kwargs)

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

