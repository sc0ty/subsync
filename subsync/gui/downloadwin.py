import gui.downloadwin_layout
import gui.errorwin
import wx
import assets
from utils import fileSizeFmt


class DownloadWin(gui.downloadwin_layout.DownloadWin):
    def __init__(self, parent, downloader, title, allowHide=False):
        super().__init__(parent)

        self.downloader = downloader
        self.state = None

        self.m_textName.SetLabel(title)
        self.m_buttonHide.Show(allowHide)
        self.updateStatus(downloader.getState())

        self.updateTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onUpdateTimerTick, self.updateTimer)
        self.updateTimer.Start(200)

    def onButtonCancelClick(self, event):
        self.downloader.stop()
        self.EndModal(wx.ID_CANCEL)

    def onButtonHideClick(self, event):
        self.EndModal(wx.ID_CLOSE)

    def onUpdateTimerTick(self, event):
        state = self.downloader.getState()
        if state and self.state != state:
            self.state = state
            self.updateStatus(state)

            if state.error and self.IsModal():
                gui.errorwin.showExceptionDlg(self, state.error)

            if state.terminated:
                self.updateTimer.Stop()
                if state.error == None and self.IsModal():
                    self.EndModal(wx.ID_OK)

    def updateStatus(self, state):
        msgs = {
                'download': _('downloading'),
                'verify':   _('verifying'),
                'install':  _('processing'),
                'done':     _('done'),
                'error':    _('operation failed') }

        msg = msgs.get(state.action, _('error'))
        self.setDetailMessage(msg, state.progress, not state.terminated)
        self.setProgress(state.progress)

    def setDetailMessage(self, msg, progress, appendProgress=True):
        if appendProgress:
            if type(progress) is tuple:
                pos, size = progress
                if size != None and size != 0:
                    msg += ' {} / {}'.format(fileSizeFmt(pos), fileSizeFmt(size))
                else:
                    msg += ' {}'.format(fileSizeFmt(pos))
            else:
                msg += '...'
        self.m_textDetails.SetLabel(msg)

    def setProgress(self, progress):
        pr = None
        if type(progress) is tuple:
            pos, size = progress
            if size != None and size != 0:
                self.m_gaugeProgress.SetValue(min(100, int(100.0 * pos / size)))
            else:
                self.m_gaugeProgress.Pulse()
        elif progress != None:
            self.m_gaugeProgress.SetValue(min(100, int(100.0 * progress)))


class UpdateWin(DownloadWin):
    def __init__(self, parent, allowHide=False):
        title = _('Application upgrade')
        super().__init__(parent, assets.updateDownloader, title, allowHide)

