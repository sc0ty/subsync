"""Assets management functionality"""

from subsync.assets.mgr import AssetManager
from subsync.assets.assetlist import AssetList

__all__ = [ 'assetManager', 'getAsset', 'AssetList' ]


def assetManager():
    """Get `subsync.assets.mgr.AssetManager` instance."""
    return AssetManager.instance()

def getAsset(assetId, params=None):
    """Get asset, alias to `assetManager().getAsset`."""
    return assetManager().getAsset(assetId, params)

