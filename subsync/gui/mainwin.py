import subsync.gui.layout.mainwin
import wx
from subsync.gui.syncwin import SyncWin
from subsync.gui.settingswin import SettingsWin
from subsync.gui.downloadwin import DownloadWin, SelfUpdateWin
from subsync.gui.aboutwin import AboutWin
from subsync.gui.busydlg import BusyDlg
from subsync.gui.errorwin import error_dlg
from subsync.assets import assetManager
from subsync import cache
from subsync import img
from subsync import config
from subsync import loggercfg
from subsync.settings import settings
from subsync.error import Error
import sys

import logging
logger = logging.getLogger(__name__)


def logRunCmd(sub, ref):
    def quoted(v):   return '"{}"'.format(v) if v else None
    def nonempty(v): return v if v else None
    def fps(v):      return '{:.5g}'.format(v) if v else None
    def channels(v): return str(v) if (v and v.type != 'auto') else None

    args = [('--sub',          quoted(sub.path)),
            ('--sub-stream',   sub.no + 1),
            ('--sub-lang',     nonempty(sub.lang)),
            ('--sub-enc',      nonempty(sub.enc)),
            ('--sub-fps',      fps(sub.fps)),
            ('--ref',          quoted(ref.path)),
            ('--ref-stream',   ref.no + 1),
            ('--ref-lang',     nonempty(ref.lang)),
            ('--ref-enc',      nonempty(ref.enc)),
            ('--ref-fps',      fps(ref.fps)),
            ('--ref-channels', channels(ref.channels)),
            ]

    cmd = [ '{}={}'.format(*arg) for arg in args if arg[1] != None ]
    logging.getLogger('RUNCMD').info('%s %s', sys.argv[0], ' '.join(cmd))


class MainWin(subsync.gui.layout.mainwin.MainWin):
    def __init__(self, parent, subs=None, refs=None):
        super().__init__(parent)

        img.setWinIcon(self)
        self.m_buttonMenu.SetLabel(u'\u22ee') # 2630
        self.m_panelMain.GetSizer().SetSizeHints(self)

        if config.assetupd == None:
            self.m_menu.Remove(self.m_menuItemCheckUpdate.GetId())

        self.m_panelSub.setStream(subs)
        self.m_panelSub.stream.types = ('subtitle/text',)

        self.m_panelRef.setStream(refs)
        self.m_panelRef.stream.types = ('subtitle/text', 'audio')

        self.m_sliderMaxDist.SetValue(settings().windowSize / 60.0)
        self.onSliderMaxDistScroll(None)

        self.Fit()
        self.Layout()

        # allow only to resize horizontally
        size = self.GetSize()
        self.SetSizeHints(minW=size.GetWidth(), minH=size.GetHeight(),
                maxH=size.GetHeight())

        self.refsCache = cache.WordsCache()
        assetManager.updateTask.start()

    def onSliderMaxDistScroll(self, event):
        val = self.m_sliderMaxDist.GetValue()
        self.m_textMaxDist.SetLabel(_('{} min').format(val))
        settings().set(windowSize=val * 60.0)

    def onButtonMenuClick(self, event):
        self.PopupMenu(self.m_menu)

    def onMenuItemSettingsClick(self, event):
        with SettingsWin(self, settings(), self.refsCache) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                newSettings = dlg.getSettings()
                if settings() != newSettings:
                    self.changeSettings(newSettings)

    def changeSettings(self, newSettings):
        if not settings().refsCache:
            self.refsCache.clear()

        if settings().logLevel != newSettings.logLevel:
            loggercfg.setLevel(newSettings.logLevel)

        if settings().logBlacklist != newSettings.logBlacklist:
            loggercfg.setBlacklistFilters(newSettings.logBlacklist)

        if settings().language != newSettings.language:
            dlg = wx.MessageDialog(
                self,
                _('Language changes will take effect after application restart'),
                _('Settings'),
                wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()

        settings().set(**newSettings.items())
        settings().save()


    def onMenuItemCheckUpdateClick(self, event):
        updAsset = assetManager.getSelfUpdaterAsset()
        hasLocalUpdate = updAsset and updAsset.hasLocalUpdate()

        if not assetManager.updateTask.isRunning() and not hasLocalUpdate:
            assetManager.updateTask.start()

        if assetManager.updateTask.isRunning():
            with BusyDlg(self, _('Checking for update...')):
                while assetManager.updateTask.isRunning():
                    wx.Yield()

        if self.runUpdater():
            self.Close(force=True)

        else:
            dlg = wx.MessageDialog(
                    self,
                    _('Your version is up to date'),
                    _('Upgrade'),
                    wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()

    def onMenuItemAboutClick(self, event):
        AboutWin(self).ShowModal()

    def onButtonCloseClick(self, event):
        self.Close()

    @error_dlg
    def onButtonStartClick(self, event):
        try:
            settings().save()
            self.start()
        except:
            self.refsCache.clear()
            raise

    def start(self, listener=None):
        self.validateSelection()
        logRunCmd(self.m_panelSub.stream, self.m_panelRef.stream)

        if self.validateAssets():
            sub = self.m_panelSub.stream
            ref = self.m_panelRef.stream
            cache = self.refsCache if settings().refsCache else None

            with SyncWin(self, sub, ref, cache, listener) as dlg:
                dlg.ShowModal()

            if listener:
                listener.onSynchronizationExit(self)

    def validateSelection(self):
        subs = self.m_panelSub.stream
        refs = self.m_panelRef.stream
        if subs.path == None or subs.no == None:
            raise Error(_('Subtitles not set'))
        if refs.path == None or refs.no == None:
            raise Error(_('Reference file not set'))
        if subs.path == refs.path and subs.no == refs.no:
            raise Error(_('Subtitles can\'t be the same as reference'))
        if refs.type == 'audio' and not refs.lang:
            raise Error(_('Select reference language first'))

    def validateAssets(self):
        subs = self.m_panelSub.stream
        refs = self.m_panelRef.stream

        needAssets = []
        if refs.type == 'audio':
            needAssets.append(assetManager.getAsset('speech', [refs.lang]))
        if subs.lang and refs.lang and subs.lang != refs.lang:
            langs = sorted([subs.lang, refs.lang])
            needAssets.append(assetManager.getAsset('dict', langs))

        missingAssets  = [ asset for asset in needAssets if not asset.isLocal() ]
        downloadAssets = [ asset for asset in missingAssets if asset.isRemote() ]
        if downloadAssets:
            if not self.askForDownloadAssets(downloadAssets):
                return False

        updateAssets = [ asset for asset in needAssets
                if asset.remoteVersion() > asset.localVersion()
                and asset not in downloadAssets ]
        if updateAssets:
            self.askForUpdateAssets(updateAssets)

        return True

    def askForDownloadAssets(self, assetList):
        msg  = [ _('Following assets must be download to continue:') ]
        msg += [ ' - ' + asset.getPrettyName() for asset in assetList ]
        msg += [ '', _('Download now?') ]
        title = _('Download assets')
        flags = wx.YES_NO | wx.ICON_QUESTION
        with wx.MessageDialog(self, '\n'.join(msg), title, flags) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                return self.downloadAssets(assetList)
        return False

    def askForUpdateAssets(self, assetList):
        msg  = [ _('Following assets could be updated:') ]
        msg += [ ' - ' + asset.getPrettyName() for asset in assetList ]
        msg += [ '', _('Update now?') ]
        title = _('Update assets')
        flags = wx.YES_NO | wx.ICON_QUESTION
        with wx.MessageDialog(self, '\n'.join(msg), title, flags) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                self.refsCache.clear()
                return self.downloadAssets(assetList)
        return False

    def downloadAssets(self, assetList):
        for asset in assetList:
            upd = asset.getUpdater()
            if not upd:
                return False

            upd.start()
            with DownloadWin(self, asset.getPrettyName(), upd) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return False
        return True

    @error_dlg
    def onClose(self, event):
        if event.CanVeto() and settings().askForUpdate:
            updAsset = assetManager.getSelfUpdaterAsset()

            if updAsset and updAsset.hasUpdate():
                dlg = wx.MessageDialog(
                        self,
                        _('New version is available. Update now?'),
                        _('Upgrade'),
                        wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

                if dlg.ShowModal() == wx.ID_YES:
                    self.runUpdater(False)

        assetManager.updateTask.stop()
        event.Skip()

    def runUpdater(self, askForUpdate=True):
        updAsset = assetManager.getSelfUpdaterAsset()
        if updAsset and updAsset.hasUpdate():
            if not updAsset.hasLocalUpdate():
                SelfUpdateWin(self).ShowModal()

                if askForUpdate:
                    dlg = wx.MessageDialog(
                            self,
                            _('New version is ready to be installed. Upgrade now?'),
                            _('Upgrade'),
                            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                    if dlg.ShowModal != wx.ID_YES:
                        return False

            if updAsset.hasLocalUpdate():
                updAsset.installUpdate()
                return True
        return False

