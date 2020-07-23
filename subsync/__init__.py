"""Subtitle Speech Synchronizer https://subsync.online

This is an automatic movie subtitle synchronization library.
"""

import gizmo
from .synchro import SyncController, SyncTask, InputFile, SubFile, RefFile, OutputFile
from .assets import assetManager, AssetList

__all__ = [
        'synchronize', 'version', 'subsync',
        'SyncController', 'SyncTask',
        'InputFile', 'SubFile', 'RefFile', 'OutputFile',
        'assetManager', 'AssetList',
        ]

__pdoc__ = { key: False for key in [
        'cli', 'cmdargs', 'config', 'data', 'error', 'gui', 'img', 'loggercfg',
        'pubkey', 'settings', 'subtitle', 'thread', 'translations', 'utils',
        'validator',
        ]}


def synchronize(sub, ref, out, *, onError=None, options={}, offline=False, updateAssets=True):
    """Synchronize single subtitle file.

    This is simplified high level synchronization API. For finer-grained
    control use `SyncController` object.

    Parameters
    ----------
    sub: SubFile or InputFile or dict
        Input subtitle description, proper object instance or `dict` with
        fields same as arguments to `InputFile` constructor.
    ref: RefFile or InputFile or dict
        Reference description, proper object instance or `dict` with fields
        same as arguments to `InputFile` constructor.
    out: OutputFile or dict
        Output subtitle description, proper object instance or `dict` with
        fields same as arguments to `OutputFile` constructor.
    onError: callable, optional
        Error callback for non-terminal errors. Terminal errors will raise
        exception. For details see `SyncController` constructor.
    options: dict, optional
        Override default synchronization options, see `SyncController.configure`.
    offline: bool, optional
        Prevent any communication with asset server. If required assets are
        missing, they will not be downloaded and synchronization will fail.
    updateAssets: bool, optional
        Whether to update existing assets if update is available online. Has no
        effect with `offline`=`True`.

    Returns
    -------
    tuple of (subsync.synchro.controller.SyncJobResult, subsync.synchro.controller.SyncStatus)
        Synchronization result.

    Notes
    -----
    This function runs synchronously - it will block until synchronization
    finishes. For non-blocking synchronization use `SyncController` instead.

    Example
    -------
    >>> sub = { 'path': './sub.srt', 'lang': 'rus' }
    >>> ref = { 'path': './movie.avi', 'stream': 2, 'lang': 'eng' }
    >>> out = { 'path': './out.srt' }
    >>> subsync.synchronize(sub, ref, out)
    (SyncJobResult(success=True, terminated=False, path='out.srt'), SyncStatus(correlated=True, maxChange=0.010168457031248579, progress=0.5212266710947953, factor=0.9999998222916713, points=289, formula=1.0000x+0.010, effort=0.5004523633099243))
    """
    task = SyncTask(sub, ref, out)
    assets = assetManager().getAssetsForTasks([ task ])

    if not offline and (assets.missing() or updateAssets):
        listUpdater = assetManager().getAssetListUpdater()
        if not listUpdater.isRunning() and not listUpdater.isUpdated():
            listUpdater.run()
            listUpdater.wait()

    assets.validate()

    if not offline:
        if updateAssets:
            downloadAssets = assets.hasUpdate()
        else:
            downloadAssets = assets.notInstalled()

        for asset in downloadAssets:
            downloader = asset.downloader()
            try:
                downloader.run()
                downloader.wait(reraise=True)
            except:
                downloader.terminate()
                raise

    assets.validate(localOnly=True)

    res = (None, None)
    def onJobEnd(task, status, result):
        nonlocal res
        res = (result, status)

    sync = SyncController(onJobEnd=onJobEnd, onError=onError)

    try:
        sync.configure(**options)
        sync.synchronize(task)
        sync.wait()
    except:
        sync.terminate()
        raise

    return res


def version():
    """Get subsync version.

    Returns
    -------
    tuple of str
        Tuple of two strings (short, long):

        - short - numbers separated by dot in format `major.minor` or `major.minor.revision`;
        - long - descriptive string.

    Example
    -------
    >>> subsync.version()
    ('0.15.34', '0.15-34-g5aa31da')
    """
    try:
        from .version import version, version_short
        return version_short, version
    except:
        return None, 'UNDEFINED'


def subsync(argv):
    """Run subsync with list of command line arguments.

    .. deprecated:: 0.16.0
    Use either `synchronize` or `SyncController` instead.
    """
    from .__main__ import subsync
    return subsync(argv)
