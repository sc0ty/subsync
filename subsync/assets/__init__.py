from subsync.assets.mgr import AssetManager
from subsync.assets.listupdater import AssetListUpdater


assetManager = AssetManager()
assetListUpdater = AssetListUpdater(assetManager)


def getAsset(assetId, params=None):
    return assetManager.getAsset(assetId, params)

