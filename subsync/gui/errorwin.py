import wx
import wx.lib.dialogs
import subsync.gui.layout.errorwin
from subsync import error
import traceback
import sys
from functools import wraps

import logging
logger = logging.getLogger(__name__)


class ErrorWin(subsync.gui.layout.errorwin.ErrorWin):
    def __init__(self, parent, msg):
        super().__init__(parent)
        self.m_textMsg.SetLabel(msg)
        self.m_textMsg.Wrap(600)
        self.Fit()
        self.Layout()
        self.Centre(wx.BOTH)

        self.msg = msg
        self.details = [ msg, '\n\n' ]

    def addDetails(self, *args):
        self.details += args

    def onTextDetailsClick(self, event):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, ''.join(self.details),
                _('Error'), size=(800, 500), style=wx.DEFAULT_FRAME_STYLE)
        font = wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dlg.SetFont(font)
        dlg.ShowModal()


def showExceptionDlg(parent=None, excInfo=None, msg=None):
    def showDlg(msg):
        if not msg:
            msg = error.getExceptionMessage(exc)
        with ErrorWin(parent, msg) as dlg:
            dlg.addDetails(*traceback.format_exception(type, exc, tb))
            dlg.ShowModal()

    if excInfo:
        type, exc, tb = excInfo
    else:
        type, exc, tb = sys.exc_info()

    if exc:
        if wx.IsMainThread():
            showDlg(msg)
        else:
            wx.CallAfter(showDlg, msg)


def error_dlg(func):
    '''Catch exceptions of type error.Error and gizmo.Error
    and show them in error window
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logger.warn('error_dlg: %r', err, exc_info=True)

            if len(args) > 0 and isinstance(args[0], wx.Window):
                parent = args[0]
            else:
                parent = None

            showExceptionDlg(parent)
    return wrapper

