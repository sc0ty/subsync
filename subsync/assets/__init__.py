import config
import utils
from assets.assets import Assets
from assets.updater import Updater
from assets.downloader import Downloader

assets = Assets()
updater = Updater()
updateDownloader = None


def init(autoUpdate):

    def onAssetsUpdated(err):
        global updateDownloader
        if config.assetupd:
            cv = utils.getCurrentVersion()
            asset = getRemoteAsset(**config.assetupd)
            if cv and asset and not isUpdateDownloadInProgress():
                rv = utils.parvseVersion(asset.get('version', None))
                if updater.version == None or updater.version < rv:
                    if not updater.upgradeReady and rv and rv > cv:
                        updateDownloader = Downloader(**asset)
                        if autoUpdate:
                            updateDownloader.start(name='Updater', daemon=False)

    assets.update(onFinish=onAssetsUpdated, delay=5)


def terminate():
    if updateDownloader:
        updateDownloader.stop(block=True)


def getLocalAsset(*args, **kwargs):
    return assets.getLocalAsset(*args, **kwargs)


def getRemoteAsset(*args, **kwargs):
    return assets.getRemoteAsset(*args, **kwargs)


def isUpdateDownloadInProgress():
    return updateDownloader and updateDownloader.isAlive()

