import wx
from subsync.gui.downloadwin import DownloadWin
from subsync.gui.busydlg import BusyDlg
from subsync.gui.components import popups
from subsync.assets import assetManager, assetListUpdater
from subsync.data import descriptions, languages
from subsync.settings import settings
from subsync.error import Error


def validateAssets(parent, tasks, updateAssets=True, askForLang=True):
    for task in tasks:
        sub = task.sub
        ref = task.ref

        if sub == None or sub.path == None or sub.no == None:
            raise raiseTaskError(task, _('Subtitles not set'))
        if ref == None or ref.path == None or ref.no == None:
            raise raiseTaskError(task, _('Reference file not set'))
        if sub.path == ref.path and sub.no == ref.no:
            raise raiseTaskError(task, _('Subtitles can\'t be the same as reference'))
        if ref.type == 'audio' and not ref.lang:
            raise raiseTaskError(task, _('Select reference language first'))
        if task.out and task.out.path:
            task.out.validateOutputPattern()

    if askForLang and settings().showLanguageNotSelectedPopup:
        if not askForLangSelection(parent, tasks):
            return False

    needed = set()
    for task in tasks:
        needed |= assetManager.getAssetsForTask(task)
    missing = [ asset for asset in needed if asset.isMissing() ]

    if missing and updateAssetList(parent):
        missing = [ asset for asset in needed if asset.isMissing() ]
        if missing:
            raiseNotSupportedAssets(missing)

    if not missing:
        nonLocal = [ asset for asset in needed if not asset.isLocal() ]
        if nonLocal:
            if not askForDownloadAssets(parent, nonLocal):
                return False

    missing = [ asset for asset in needed if not asset.isLocal() ]
    if missing:
        raiseMissingAssets(missing)

    if updateAssets:
        update = [ asset for asset in needed if asset.isUpgradable() ]
        if update:
            askForUpdateAssets(parent, update)

    return True

def updateAssetList(parent):
    if not assetListUpdater.isRunning() and not assetListUpdater.isListReady:
        assetListUpdater.start(autoUpdate=False)

    with BusyDlg(parent, _('Downloading assets list...'), cancellable=True) as dlg:
        if dlg.ShowModalWhile(assetListUpdater.isRunning) == wx.ID_OK:
            return assetListUpdater.hasList()
        else:
            assetListUpdater.stop()

def raiseNotSupportedAssets(assets):
    msg  = []
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

def raiseMissingAssets(assets):
    msg  = [ _('Following assets are missing:') ]
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
        upd = asset.getUpdater()
        if not upd:
            return False

        upd.start()
        with DownloadWin(parent, asset.getPrettyName(), upd) as dlg:
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

def raiseTaskError(task, msg):
    msgs = [ msg, '' ]
    if task.sub and task.sub.path:
        msgs.append(_('subtitles: ') + task.sub.path)
    if task.ref and task.ref.path:
        msgs.append(_('references: ') + task.ref.path)
    if task.out and task.out.path:
        msgs.append(_('output: ') + task.out.path)

    raise Error('\n'.join(msgs)) \
            .addn('sub', task.sub) \
            .addn('ref', task.ref) \
            .addn('out', task.out)
