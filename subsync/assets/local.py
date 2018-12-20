from subsync import assets
from subsync import config
from subsync import error
import os
import itertools


def getAsset(type, params, permutable=False, raiseIfMissing=False):
    if permutable:
        paramsPerm = itertools.permutations(params)
    else:
        paramsPerm = [ params ]

    for params in paramsPerm:
        fname = '{}.{}'.format('-'.join(params), type)
        path = os.path.join(config.assetdir, type, fname)
        if os.path.isfile(path):
            return path

    if raiseIfMissing:
        raise error.Error(_('Missing {}').format(
            assets.getAssetPrettyName(type, params)),
            type=type, params=params)

