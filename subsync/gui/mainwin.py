import gui.mainwin_layout
import wx
from gui.syncwin import SyncWin
from gui.settingswin import SettingsWin
from gui.downloadwin import DownloadWin, UpdateWin
from gui.aboutwin import AboutWin
from gui.errorwin import error_dlg
import assets
import img
import config
import loggercfg
from settings import settings
from error import Error

import logging
logger = logging.getLogger(__name__)


def logRunCmd(sub, ref):
    args = [('--sub',        '"{}"'.format(sub.path)),
            ('--sub-stream', sub.no + 1),
            ('--sub-lang',   sub.lang),
            ('--sub-enc',    sub.enc),
            ('--ref',        '"{}"'.format(ref.path)),
            ('--ref-stream', ref.no + 1),
            ('--ref-lang',   ref.lang),
            ('--ref-enc',    ref.enc),
            ('--ref-fps',    ref.fps)  ]

    cmd = [ '{}={}'.format(*arg)
            for arg in args
            if arg[1] != None and arg[1] != '' ]

    logger.info('run command: subsync %s', ' '.join(cmd))


class MainWin(gui.mainwin_layout.MainWin):
    def __init__(self, parent, subs=None, refs=None):
        gui.mainwin_layout.MainWin.__init__(self, parent)

        img.setWinIcon(self)
        self.m_buttonMenu.SetLabel(u'\u2630')
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

    '''
    def reload(self):
        subs = self.m_panelSub.stream
        refs = self.m_panelRef.stream
        self.Unbind(wx.EVT_CLOSE)
        self.Close(force=True)
        win = MainWin(None, subs, refs)
        win.Show()
    '''

    def onSliderMaxDistScroll(self, event):
        val = self.m_sliderMaxDist.GetValue()
        self.m_textMaxDist.SetLabel(_('{} min').format(val))
        settings().set(windowSize=val * 60.0)

    def onButtonMenuClick(self, event):
        self.PopupMenu(self.m_menu)

    def onMenuItemSettingsClick(self, event):
        with SettingsWin(self, settings()) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                newSettings = dlg.getSettings()

                if settings().logLevel != newSettings.logLevel:
                    loggercfg.setLevel(newSettings.logLevel)

                if settings().logBlacklist != newSettings.logBlacklist:
                    loggercfg.setBlacklistFilters(newSettings.logBlacklist)

                if settings() != newSettings:
                    settings().set(**newSettings.items())
                    settings().save()

    def onMenuItemCheckUpdateClick(self, event):
        if assets.isUpdateDownloadInProgress():
            if UpdateWin(self, allowHide=True).ShowModal() != wx.ID_OK:
                return

        assets.updater.load()
        if assets.updater.upgradeReady:
            if askForUpdate(self):
                assets.updater.upgrade()
                self.Unbind(wx.EVT_CLOSE)
                self.Close(force=True)
        else:
            dlg = wx.MessageDialog(
                    self,
                    _('There is no upgrade available'),
                    _('Upgrade'),
                    wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()

    def onMenuItemAboutClick(self, event):
        AboutWin(self).ShowModal()

    def onButtonCloseClick(self, event):
        self.Close()

    @error_dlg
    def onButtonStartClick(self, event):
        settings().save()
        self.validateSelection()
        logRunCmd(self.m_panelSub.stream, self.m_panelRef.stream)

        if self.validateAssets():
            sub = self.m_panelSub.stream
            ref = self.m_panelRef.stream
            dlg = SyncWin(self, sub, ref)
            dlg.ShowModal()

    def validateSelection(self):
        subs = self.m_panelSub.stream
        refs = self.m_panelRef.stream
        if subs.path == None or subs.no == None:
            raise Error(_('Subtitles not set'))
        if refs.path == None or refs.no == None:
            raise Error(_('Reference file not set'))
        if subs.path == refs.path and subs.no == refs.no:
            raise Error(_('Subtitles can\'t be the same as reference'))
        if not (subs.lang == None and refs.lang == None):
            if subs.lang == None:
                raise Error(_('Select subtitles language first'))
            if refs.lang == None:
                raise Error(_('Select reference language first'))

    def validateAssets(self):
        subs = self.m_panelSub.stream
        refs = self.m_panelRef.stream

        needAssets = []
        if refs.type == 'audio':
            needAssets.append(dict(type='speech', params=[refs.lang]))
        if subs.lang and refs.lang and subs.lang != refs.lang:
            needAssets.append(dict(type='dict', params=[subs.lang, refs.lang],
                permutable=True))

        missingAssets = [ a for a in needAssets if assets.getLocalAsset(**a) == None ]
        if len(missingAssets) == 0:
            return True

        downloadAssets = []
        for id in missingAssets:
            asset = assets.assets.getRemoteAsset(**id, raiseIfMissing=True)
            downloadAssets.append(asset)

        msg = _('Following assets must be download to continue:\n')
        msg += '\n'.join([' - ' + asset['title'] for asset in downloadAssets])
        msg += '\n\n' + _('Download now?')
        title = _('Download assets')
        with wx.MessageDialog(self, msg, title, wx.YES_NO | wx.ICON_QUESTION) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                return self.downloadAssets(downloadAssets)

    def downloadAssets(self, assetsl):
        for asset in assetsl:
            down = assets.Downloader(**asset)
            down.start(name='AssetDown', daemon=False)
            title = asset['title']

            with DownloadWin(self, down, title=title) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return False
        return True

    @error_dlg
    def onClose(self, event):
        if assets.isUpdateDownloadInProgress() and not askForUpdateTermination(self):
            UpdateWin(self, allowHide=event.CanVeto()).ShowModal()
            event.Veto()

        if settings().askForUpdate and not assets.isUpdateDownloadInProgress():
            assets.updater.load()
            if assets.updater.upgradeReady and askForUpdate(self):
                assets.updater.upgrade()
                event.Veto(False)

        if not event.GetVeto():
            event.Skip()


def askForUpdateTermination(parent):
    dlg = wx.MessageDialog(
            parent,
            _('Update is being download, do you want to terminate?'),
            _('Upgrade'),
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    return dlg.ShowModal() == wx.ID_YES


def askForUpdate(parent):
    dlg = wx.MessageDialog(
            parent,
            _('New version is ready to be installed. Upgrade now?'),
            _('Upgrade'),
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
    return dlg.ShowModal() == wx.ID_YES

