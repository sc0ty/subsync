import subsync.gui.layout.downloadwin
from subsync.gui import errorwin
import wx
from subsync.assets import assetManager
from subsync.gui.components.thread import gui_thread
from subsync import utils
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


class DownloadWin(subsync.gui.layout.downloadwin.DownloadWin):
    def __init__(self, parent, title, updater):
        super().__init__(parent)
        self.m_textName.SetLabel(title)

        status = updater.getStatus()
        if not status.state == 'run' and not (status.state == 'done' and status.detail == 'success'):
            updater.start()

        self.updater = updater
        self.lastPos = None

        self.progressTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onProgressTimerTick, self.progressTimer)
        self.progressTimer.Start(200)

    def ShowModal(self):
        res = super().ShowModal()
        self.onClose(None)
        return res

    def onClose(self, event):
        self.updater.stop()
        if self.progressTimer.IsRunning():
            self.progressTimer.Stop()

    def onProgressTimerTick(self, event):
        status = self.updater.getStatus()

        if status.state == 'run':
            if status.detail == 'download':
                self.setStatus(_('downloading'), status.progress)
            else:
                self.setStatus(_('processing...'))
            self.setProgress(status.progress)

        elif status.state == 'done':
            self.progressTimer.Stop()
            res = None

            if status.detail == 'success':
                self.setStatus(_('operation finished successfully'))
                self.setProgress(1)
                res = wx.ID_OK

            elif status.detail == 'fail':
                self.setStatus(_('operation failed'))
                if status.error is not None:
                    errorwin.showExceptionDlg(self, status.error)
                res = wx.ID_CANCEL

            elif status.detail == 'cancel':
                self.setStatus(_('operation cancelled by the user'))
                res = wx.ID_CANCEL

            wx.Yield()

            if self.IsModal():
                self.EndModal(res)

    def setStatus(self, desc, progress=None):
        msg = [ desc ]
        if progress is not None:
            pos, size = progress
            msg += [ utils.fileSizeFmt(pos) ]
            if size != None:
                msg += [ '/', utils.fileSizeFmt(size) ]
            msg += [ self.getDownloadSpeed(pos) ]
        self.m_textDetails.SetLabel(' '.join(msg))

    def setProgress(self, progress):
        if isinstance(progress, tuple):
            pos, size = progress
        else:
            pos, size = progress, 1

        if pos is None or size is None:
            self.m_gaugeProgress.Pulse()
        else:
            p = max(min(pos / size, 1.0), 0.0)
            self.m_gaugeProgress.SetValue(int(100.0 * p))

    def getDownloadSpeed(self, pos):
        res = ''
        if pos != None and self.lastPos != None:
            delta = pos - self.lastPos
            if delta > 0:
                interval = self.progressTimer.GetInterval() / 1000.0
                res = '({}/s)'.format(utils.fileSizeFmt(delta / interval))
        self.lastPos = pos
        return res

    @gui_thread
    def onUpdateComplete(self, upd, success):
        if success:
            self.setProgress(1.0)
            self.setStatus('operation finished successfully')
            if self.IsModal():
                self.EndModal(wx.ID_OK)
        else:
            self.setStatus('operation failed')
            if self.IsModal():
                self.EndModal(wx.ID_CANCEL)


class SelfUpdateWin(DownloadWin):
    def __init__(self, parent):
        title = _('Application upgrade')
        asset = assetManager.getSelfUpdaterAsset()
        updater = asset and asset.getUpdater()
        if not updater:
            raise Error('Application upgrade is not available')

        super().__init__(parent, title, updater)
