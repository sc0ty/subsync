import subsync.gui.layout.mainwin
import wx
from subsync.gui.syncwin import SyncWin
from subsync.gui.settingswin import SettingsWin
from subsync.gui.downloadwin import SelfUpdateWin
from subsync.gui.aboutwin import AboutWin
from subsync.gui.components import assetsdlg
from subsync.gui.busydlg import BusyDlg
from subsync.gui.errorwin import error_dlg
from subsync.synchro import SyncTask
from subsync.assets import assetManager
from subsync import cache
from subsync import img
from subsync import config
from subsync import loggercfg
from subsync.settings import settings
import sys

import logging
logger = logging.getLogger(__name__)


def logRunCmd(task):
    def quoted(v):   return '"{}"'.format(v) if v else None
    def nonempty(v): return v if v else None
    def fps(v):      return '{:.5g}'.format(v) if v else None
    def channels(v): return v.serialize() if (v and v.type != 'auto') else None

    args = []
    if task.sub: args += [
            ('--sub',          quoted(task.sub.path)),
            ('--sub-stream',   task.sub.no + 1),
            ('--sub-lang',     nonempty(task.sub.lang)),
            ('--sub-enc',      nonempty(task.sub.enc)),
            ('--sub-fps',      fps(task.sub.fps)),
            ]
    if task.ref: args += [
            ('--ref',          quoted(task.ref.path)),
            ('--ref-stream',   task.ref.no + 1),
            ('--ref-lang',     nonempty(task.ref.lang)),
            ('--ref-enc',      nonempty(task.ref.enc)),
            ('--ref-fps',      fps(task.ref.fps)),
            ('--ref-channels', channels(task.ref.channels)),
            ]
    if task.out: args += [
            ('--out',          quoted(task.out.path)),
            ('--out-enc',      nonempty(task.out.enc)),
            ('--out-fps',      fps(task.out.fps)),
            ]

    cmd = [ '{}={}'.format(*arg) for arg in args if arg[1] != None ]
    logging.getLogger('RUNCMD').info('%s %s', sys.argv[0], ' '.join(cmd))


class MainWin(subsync.gui.layout.mainwin.MainWin):
    def __init__(self, parent, sub=None, ref=None):
        super().__init__(parent)

        img.setWinIcon(self)
        self.m_buttonMenu.SetLabel(u'\u22ee') # 2630
        self.m_panelMain.GetSizer().SetSizeHints(self)

        if config.assetupd == None:
            self.m_menu.Remove(self.m_menuItemCheckUpdate.GetId())

        self.m_panelSub.setStream(sub)
        self.m_panelRef.setStream(ref)

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
            # TODO: update to new BusyDlg
            with BusyDlg(self, _('Checking for update...')) as dlg:
                dlg.ShowModalWhile(assetManager.updateTask.isRunning)

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
            task = SyncTask(self.m_panelSub.stream, self.m_panelRef.stream)
            self.start(task)
        except:
            self.refsCache.clear()
            raise

    def start(self, task, auto=None):
        if assetsdlg.validateAssets(self, [task]):
            logRunCmd(task)
            cache = self.refsCache if settings().refsCache else None

            with SyncWin(self, task, auto=auto, refCache=cache) as dlg:
                dlg.ShowModal()

        if auto == 'done':
            self.Close()

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

