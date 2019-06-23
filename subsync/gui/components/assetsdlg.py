import wx
from subsync.gui.downloadwin import DownloadWin
from subsync.assets import assetManager
from subsync.error import Error


def validateAssets(parent, tasks, update=True):
    needAssets = set()

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

        if ref.type == 'audio':
            needAssets.add(assetManager.getAsset('speech', [ref.lang]))
        if sub.lang and ref.lang and sub.lang != ref.lang:
            langs = sorted([sub.lang, ref.lang])
            needAssets.add(assetManager.getAsset('dict', langs))

    missingAssets  = [ asset for asset in needAssets if not asset.isLocal() ]
    downloadAssets = [ asset for asset in missingAssets if asset.isRemote() ]
    if downloadAssets:
        if not askForDownloadAssets(parent, downloadAssets):
            return False

    if update:
        updateAssets = [ asset for asset in needAssets
                if asset.remoteVersion() > asset.localVersion()
                and asset not in downloadAssets ]
        if updateAssets:
            askForUpdateAssets(parent, updateAssets)

    missingAssets = [ asset for asset in needAssets if not asset.isLocal() ]
    if missingAssets:
        msg = []
        if not assetManager.remoteAssetListReady:
            msg += [ _('Couldn\'t download asset list from remote server.'), '' ]
        msg += [ _('Following assets are missing:') ]
        msg += [ ' - ' + asset.getPrettyName() for asset in missingAssets ]
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
