import wx
import threading
import sys

import logging
logger = logging.getLogger(__name__)


class BusyDlg(wx.Dialog):
    def __init__(self, parent, msg):
        style = wx.BORDER_SIMPLE | wx.FRAME_TOOL_WINDOW
        if parent:
            style |= wx.FRAME_FLOAT_ON_PARENT

        super().__init__(parent, style=style)

        panel = wx.Panel(self)
        text = wx.StaticText(panel, label=msg)

        fgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        bgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        for win in [panel, text]:
            win.SetCursor(wx.HOURGLASS_CURSOR)
            win.SetForegroundColour(fgColor)
            win.SetBackgroundColour(bgColor)

        size = text.GetBestSize()
        self.SetClientSize((size.width + 80, size.height + 40))
        panel.SetSize(self.GetClientSize())
        text.Center()
        self.Center()

    def ShowModalWhile(self, condCb, checkInterval=0.1):
        self.condCb = condCb
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.checkCond, self.timer)
        self.timer.Start(checkInterval * 1000)
        return self.ShowModal()

    def checkCond(self, event):
        if not self.condCb():
            self.timer.Stop()
            self.EndModal(wx.ID_OK)


def showBusyDlgAsyncJob(parent, msg, job, *args, **kwargs):
    res = None
    exc = None

    def runJob():
        nonlocal res, exc
        try:
            res = job(*args, **kwargs)
        except Exception as err:
            logger.warn('showBusyDlgAsyncJob: %r', err, exc_info=True)
            exc = sys.exc_info()

    thread = threading.Thread(target=runJob)
    thread.start()

    with BusyDlg(parent, msg) as dlg:
        dlg.ShowModalWhile(thread.is_alive)

    if exc:
        raise exc[1]

    return res
