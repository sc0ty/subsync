import subsync.gui.layout.downloadwin
from subsync.gui import errorwin
import wx
from subsync.assets import assetManager
from subsync import thread
from subsync import utils
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


class DownloadWin(subsync.gui.layout.downloadwin.DownloadWin):
    def __init__(self, parent, title, updater):
        super().__init__(parent)
        self.m_textName.SetLabel(title)

        self.updater = updater
        self.lastPos = None

        self.progressTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onProgressTimerTick, self.progressTimer)
        self.progressTimer.Start(200)

    def ShowModal(self):
        res = super().ShowModal()

        self.updater.stop()
        if self.progressTimer.IsRunning():
            self.progressTimer.Stop()

        return res

    def onProgressTimerTick(self, event):
        done, progress, error = self.updater.getState()

        if done:
            if self.progressTimer.IsRunning():
                self.progressTimer.Stop()

            if error:
                self.setStatus(_('operation failed'))
                errorwin.showExceptionDlg(self, error)
                res = wx.ID_CANCEL

            else:
                self.setProgress(1.0)
                self.setStatus(_('operation finished successfully'))
                res = wx.ID_OK

            wx.Yield()

            if self.IsModal():
                self.EndModal(res)

        elif isinstance(progress, tuple):
            pos, size = progress
            self.setStatus(_('downloading'), pos, size)
            if size:
                self.setProgress(pos / size)
            else:
                self.setProgress(None)

        elif progress != None:
            self.setStatus(_('processing...'))
            self.setProgress(progress)

    def setStatus(self, desc, pos=None, size=None):
        msg = [ desc ]
        if pos != None:
            msg += [ utils.fileSizeFmt(pos) ]
            if size != None:
                msg += [ '/', utils.fileSizeFmt(size) ]
            msg += [ self.getDownloadSpeed(pos) ]
        self.m_textDetails.SetLabel(' '.join(msg))

    def setProgress(self, progress):
        if progress == None:
            self.m_gaugeProgress.Pulse()
        else:
            p = max(min(progress, 1.0), 0.0)
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

    @thread.gui_thread
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
        updater = asset.getUpdater() if asset else None
        if not updater:
            raise Error('Application upgrade is not available')

        super().__init__(parent, title, updater)

