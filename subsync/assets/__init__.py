from subsync.assets.mgr import AssetManager


assetManager = AssetManager()


def getAsset(assetId, params=None):
    return assetManager.getAsset(assetId, params)

