import gui.subpanel_layout
import wx
import os
from stream import Stream
from settings import settings
import gui.openwin
import gui.filedrop
from gui.errorwin import error_dlg


class SubtitlePanel(gui.subpanel_layout.SubtitlePanel):
    ''' This is subtitle or reference panel used on MainWin
    '''
    def __init__(self, parent, *args, **kwargs):
        gui.subpanel_layout.SubtitlePanel.__init__(self, parent)
        gui.filedrop.setFileDropTarget(self, self.onDropSubFile)
        self.stream = Stream()

    @error_dlg
    def onButtonSubOpenClick(self, event):
        stream = self.stream
        if not stream.isOpen():
            stream = gui.openwin.showOpenFileDlg(self, self.stream)
        self.showOpenWin(stream)

    def showOpenWin(self, stream):
        if stream != None and stream.isOpen():
            with gui.openwin.OpenWin(self, stream) as dlg:
                if dlg.ShowModal() == wx.ID_OK and dlg.stream.isOpen():
                    self.setStream(dlg.stream)

    def onChoiceSubLang(self, event):
        self.stream.lang = self.m_choiceSubLang.GetValue()

    def onDropSubFile(self, filename):

        @error_dlg
        def showOpenWinWithFile(filename):
            stream = gui.openwin.readStream(filename, self.stream.types)
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

