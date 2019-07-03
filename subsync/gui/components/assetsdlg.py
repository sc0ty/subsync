import wx
from subsync.gui.downloadwin import DownloadWin
from subsync.assets import assetManager, assetListUpdater
from subsync.error import Error


def validateAssets(parent, tasks, updateAssets=True):
    for task in tasks:
        sub = task.sub
        ref = task.ref

        if sub == None or sub.path == None or sub.no == None:
            raise Error(_('Subtitles not set')).add('ref', ref)
        if ref == None or ref.path == None or ref.no == None:
            raise Error(_('Reference file not set')).add('sub', sub)
        if sub.path == ref.path and sub.no == ref.no:
            raise Error(_('Subtitles can\'t be the same as reference')) \
                    .add('sub', sub).add('ref', ref)
        if ref.type == 'audio' and not ref.lang:
            raise Error(_('Select reference language first')).add('ref', ref)

    assetListNotReady = assetListUpdater.isRunning()

    needed = set()
    for task in tasks:
        needed |= assetManager.getAssetsForTask(task)
    missing = [ asset for asset in needed if asset.isMissing() ]

    if assetListNotReady and missing:
        with BusyDlg(self, _('Downloading assets list...')) as dlg:
            dlg.ShowModalWhile(assetListUpdater.isRunning)
        missing = [ asset for asset in needed if asset.isMissing() ]

    if missing:
        msg = [ _('Following assets are missing on server:'), '' ]
        msg += [ ' - ' + asset.getPrettyName() for asset in missing ]
        raise Error('\n'.join(msg))

    nonLocal = [ asset for asset in needed if not asset.isLocal() ]
    if nonLocal:
        if not askForDownloadAssets(parent, nonLocal):
            return False

    if updateAssets:
        update = [ asset for asset in needed if asset.isUpgradable() ]
        if update:
            askForUpdateAssets(parent, update)

    missing = [ asset for asset in needed if not asset.isLocal() ]
    if missing:
        msg = [ _('Following assets are missing:') ]
        msg += [ ' - ' + asset.getPrettyName() for asset in missing ]
        raise Error('\n'.join(msg))

    return True

def askForDownloadAssets(parent, assetList):
    msg  = [ _('Following assets must be download to continue:') ]
    msg += [ ' - ' + asset.getPrettyName() for asset in assetList ]
    msg += [ '', _('Download now?') ]
    title = _('Download assets')
    flags = wx.YES_NO | wx.ICON_QUESTION
    with wx.MessageDialog(parent, '\n'.join(msg), title, flags) as dlg:
        if dlg.ShowModal() == wx.ID_YES:
            return downloadAssets(parent, assetList)
    return False

def askForUpdateAssets(parent, assetList):
    msg  = [ _('Following assets could be updated:') ]
    msg += [ ' - ' + asset.getPrettyName() for asset in assetList ]
    msg += [ '', _('Update now?') ]
    title = _('Update assets')
    flags = wx.YES_NO | wx.ICON_QUESTION
    with wx.MessageDialog(parent, '\n'.join(msg), title, flags) as dlg:
        if dlg.ShowModal() == wx.ID_YES:
            return downloadAssets(parent, assetList)
    return False

def downloadAssets(parent, assetList):
    for asset in assetList:
        upd = asset.getUpdater()
        if not upd:
            return False

        upd.start()
        with DownloadWin(parent, asset.getPrettyName(), upd) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return False
    return True
