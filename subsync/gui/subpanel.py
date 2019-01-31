import subsync.gui.layout.subpanel
import wx
import os
from subsync.stream import Stream
from subsync.settings import settings
from subsync.gui import openwin
from subsync.gui import filedrop
from subsync.gui.errorwin import error_dlg


class SubtitlePanel(subsync.gui.layout.subpanel.SubtitlePanel):
    ''' This is subtitle or reference panel used on MainWin
    '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        filedrop.setFileDropTarget(self, self.onDropSubFile)
        self.stream = Stream()

    @error_dlg
    def onButtonSubOpenClick(self, event):
        stream = self.stream
        if not stream.isOpen():
            stream = openwin.showOpenFileDlg(self, self.stream)
        self.showOpenWin(stream)

    def showOpenWin(self, stream):
        if stream != None and stream.isOpen():
            with openwin.OpenWin(self, stream) as dlg:
                if dlg.ShowModal() == wx.ID_OK and dlg.stream.isOpen():
                    self.setStream(dlg.stream)

    def onChoiceSubLang(self, event):
        self.stream.lang = self.m_choiceSubLang.GetValue()

    def onDropSubFile(self, filename):

        @error_dlg
        def showOpenWinWithFile(filename):
            stream = openwin.readStream(self, filename, self.stream.types)
            settings().lastdir = os.path.dirname(filename)
            self.showOpenWin(stream)

        # this is workaround for Windows showing drag&drop cursor inside OpenWin
        # and locking explorer window from where the file was dragged
        wx.CallAfter(showOpenWinWithFile, filename)
        return True

    def setStream(self, stream):
        if stream != None and stream.isOpen():
            self.stream.assign(stream)
            self.m_textSubPath.SetValue('{}:{}'.format(self.stream.path, self.stream.no + 1))
            self.m_textSubPath.SetInsertionPoint(self.m_textSubPath.GetLastPosition())
            self.m_choiceSubLang.SetValue(self.stream.lang)

