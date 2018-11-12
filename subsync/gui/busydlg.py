import wx


class BusyDlg(object):
    def __init__(self, msg):
        self.msg = msg
        self.dlg = None

    def __enter__(self):
        self.dlg = wx.BusyInfo(self.msg)
        wx.Yield()

    def __exit__(self, type, value, traceback):
        del self.dlg

