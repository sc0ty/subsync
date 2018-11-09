import gui.subpanel_layout
import wx
import os
from stream import Stream
from settings import settings
from gui.openwin import OpenWin, showOpenSubFileDlg
from gui.filedrop import setFileDropTarget
from gui.errorwin import error_dlg


class SubtitlePanel(gui.subpanel_layout.SubtitlePanel):
    def __init__(self, parent, *args, **kwargs):
        wx.FileDropTarget.__init__(self)
        gui.subpanel_layout.SubtitlePanel.__init__(self, parent)
        setFileDropTarget(self, self.onDropSubFile)
        self.stream = Stream()

    @error_dlg
    def onButtonSubOpenClick(self, event):
        stream = self.stream
        if not stream.isOpen():
            stream = showOpenSubFileDlg(self, self.stream)
        self.showStreamSelectDlg(stream)

    def showStreamSelectDlg(self, stream):
        if stream != None and stream.isOpen():
            with OpenWin(self, stream) as dlg:
                if dlg.ShowModal() == wx.ID_OK and dlg.stream.isOpen():
                    self.setStream(dlg.stream)

    def onChoiceSubLang(self, event):
        self.stream.lang = self.m_choiceSubLang.GetValue()

    def onDropSubFile(self, filename):
        self.openStreamSelectDlg(filename)
        return True

    @error_dlg
    def openStreamSelectDlg(self, filename):
        stream = Stream(path=filename, types=self.stream.types)
        settings().lastdir = os.path.dirname(filename)
        self.showStreamSelectDlg(stream)

    def setStream(self, stream):
        if stream != None and stream.isOpen():
            self.stream.assign(stream)
            self.m_textSubPath.SetValue('{}:{}'.format(self.stream.path, self.stream.no + 1))
            self.m_textSubPath.SetInsertionPoint(self.m_textSubPath.GetLastPosition())
            self.m_choiceSubLang.SetValue(self.stream.lang)

