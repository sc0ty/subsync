import wx
from subsync.gui.downloadwin import DownloadWin
from subsync.gui.busydlg import BusyDlg
from subsync.gui.components import popups
from subsync.assets import assetManager
from subsync.data import descriptions, languages
from subsync.settings import settings
from subsync.error import Error


def validateAssets(parent, tasks, updateAssets=True, askForLang=True, autoSave=False):
    if askForLang and settings().showLanguageNotSelectedPopup:
        if not askForLangSelection(parent, tasks):
            return False

    assets = assetManager.getAssetsForTasks(tasks)

    if assets.notInstalled():
        updateAssetList(parent)

    if assets.missing():
        raiseNotSupportedAssets(assets.missing())

    if assets.notInstalled():
        if not askForDownloadAssets(parent, assets.notInstalled()):
            return False

    if updateAssets and assets.hasUpdate():
        askForUpdateAssets(parent, assets.hasUpdate())

    return True

def updateAssetList(parent):
    listUpdater = assetManager.getAssetListUpdater()
    if not listUpdater.isRunning() and not listUpdater.isUpdated():
        listUpdater.run()

    if listUpdater.isRunning():
        with BusyDlg(parent, _('Downloading assets list...')) as dlg:
            dlg.ShowModalWhile(listUpdater.isRunning)

    return listUpdater.isUpdated()

def raiseNotSupportedAssets(assets):
    msg = []
    speech = [ asset for asset in assets if asset.type == 'speech' ]
    dicts  = [ asset for asset in assets if asset.type == 'dict' ]

    if speech:
        langs = ', '.join([ languages.getName(a.params[0]) for a in speech ])
        msg += [ _('Synchronization with {} audio is currently not supported.') \
                .format(langs) ]
    if dicts:
        langs = [ ' - '.join([ languages.getName(p) for p in a.params ]) for a in dicts ]
        msg += [ _('Synchronization between languages {} is currently not supported.') \
                .format(', '.join(langs)) ]

    msg += [ '', _('missing assets:') ]
    msg += [ ' - ' + asset.getPrettyName() for asset in assets ]
    raise Error('\n'.join(msg))

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
        with DownloadWin(parent, asset) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return False
    return True

def askForLangSelection(parent, tasks):
    msg = [ _('No language selected for:') ]
    missingLang = False
    for task in tasks:
        if not task.sub.lang:
            msg.append(_('subtitles: ') + task.sub.path)
            missingLang = True
        if not task.ref.lang:
            msg.append(_('references: ') + task.ref.path)
            missingLang = True

    if missingLang:
        msg += [ '', descriptions.noLanguageSelectedQuestion ]
        title = _('No language selected')
        return popups.showConfirmationPopup(parent, '\n'.join(msg), title,
                confirmKey='showLanguageNotSelectedPopup')

    return True
