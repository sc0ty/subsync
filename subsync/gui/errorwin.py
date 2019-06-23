import wx
import wx.lib.dialogs
import subsync.gui.layout.errorwin
from subsync import error
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

        # workaround for window not resized
        wx.CallAfter(self.Fit)

        self.msg = msg
        self.details = [ msg, '\n\n' ]

    def addDetails(self, *args):
        for arg in args:
            self.details += arg
            if arg and arg[-1] not in [ '\n', '\r' ]:
                self.details += '\n'

    def onTextDetailsClick(self, event):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, ''.join(self.details),
                _('Error'), size=(800, 500), style=wx.DEFAULT_FRAME_STYLE)
        font = wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dlg.SetFont(font)
        dlg.ShowModal()
        self.EndModal(wx.ID_OK)


def showExceptionDlg(parent=None, excInfo=None, msg=None):
    def showDlg(msg, details):
        with ErrorWin(parent, msg) as dlg:
            dlg.addDetails(details)
            dlg.ShowModal()

    if not msg:
        msg = error.getExceptionMessage(excInfo and excInfo[1])

    details = error.getExceptionDetails(excInfo)

    if wx.IsMainThread():
        showDlg(msg, details)
    else:
        wx.CallAfter(showDlg, msg, details)


def showErrorDetailsDlg(parent, msg, title, size=(800, 500)):
    dlg = wx.lib.dialogs.ScrolledMessageDialog(parent, msg, title,
            size=size, style=wx.DEFAULT_FRAME_STYLE)
    font = wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
    dlg.SetFont(font)
    dlg.ShowModal()


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


def syncErrorToString(source, err):
    if source == 'sub':
        if err.fields.get('module', '').startswith('SubtitleDec.decode'):
            return _('Some subtitles can\'t be decoded (invalid encoding?)')
        else:
            return _('Error during subtitles read')
    elif source == 'ref':
        if err.fields.get('module', '').startswith('SubtitleDec.decode'):
            return _('Some reference subtitles can\'t be decoded (invalid encoding?)')
        else:
            return _('Error during reference read')
    elif source == 'out':
        return _('Couldn\'t save synchronized subtitles')
    else:
        return _('Unexpected error occurred')
