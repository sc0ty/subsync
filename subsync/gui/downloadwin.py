import subsync.gui.layout.downloadwin
import wx
from subsync.gui import errorwin
from subsync.gui.components.thread import gui_thread
from subsync import utils
from subsync.error import Error
import time
import sys

import logging
logger = logging.getLogger(__name__)


class DownloadWin(subsync.gui.layout.downloadwin.DownloadWin):
    def __init__(self, parent, asset):
        super().__init__(parent)
        self.m_textName.SetLabel(asset.getPrettyName())

        self.lastPos = 0
        self.startTime = time.monotonic()

        self.downloader = asset.download(
                onUpdate=self.onUpdate,
                onEnd=self.onEnd,
                timeout=0.5)

        if not self.downloader.isRunning():
            try:
                done = self.downloader.wait(reraise=True)
                exception = None
            except:
                done = False
                exception = sys.exc_info()
            wx.CallAfter(self.onEnd, asset, not done, exception)

    def ShowModal(self):
        try:
            return super().ShowModal()
        finally:
            self.onClose(None)

    def onClose(self, event):
        if self.downloader and self.downloader.isRunning():
            self.downloader.terminate()
            self.downloader.unregisterCallbacks(onUpdate=self.onUpdate, onEnd=self.onEnd)
            self.downloader = None

        if event:
            event.Skip()

    @gui_thread
    def onUpdate(self, asset, progress, size):
        msg = _('downloading')
        if progress and size:
            self.m_gaugeProgress.SetValue(int(100.0 * progress / size))
            msg = '{} {} / {} {}'.format(
                    msg,
                    utils.fileSizeFmt(progress),
                    utils.fileSizeFmt(size),
                    self.getDownloadSpeed(progress) or '')
        elif progress:
            self.m_gaugeProgress.Pulse()
            msg = '{} {} {}'.format(
                    msg,
                    utils.fileSizeFmt(progress),
                    self.getDownloadSpeed(progress) or '')
        else:
            msg = '{}...'.format(msg)
        self.m_textDetails.SetLabel(msg)

    @gui_thread
    def onEnd(self, asset, terminated, error):
        if not terminated and not error:
            self.m_gaugeProgress.SetValue(100)
            self.m_textDetails.SetLabel(_('operation finished successfully'))
            res = wx.ID_OK
        else:
            if terminated:
                self.m_textDetails.SetLabel('operation cancelled')
            elif error:
                self.m_textDetails.SetLabel(_('operation failed'))
                errorwin.showExceptionDlg(self, error)
            res = wx.ID_CANCEL

        wx.Yield()
        if self.IsModal():
            self.EndModal(res)
        else:
            self.Close()

    def getDownloadSpeed(self, pos):
        if pos is not None:
            delta = pos - self.lastPos
            if delta > 0:
                self.lastPos = pos
                now = time.monotonic()
                interval = now - self.startTime
                if interval > 0:
                    return '({})'.format(utils.transferSpeedFmt(delta, interval))
