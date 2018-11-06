import gui.openwin_layout
import wx
from stream import Stream
from gui.filedlg import showOpenFileDlg
from gui.filedrop import setFileDropTarget
from gui.errorwin import error_dlg
from error import Error
from data.filetypes import subtitleWildcard, videoWildcard


@error_dlg
def showOpenSubFileDlg(parent, stream):
    props = {}
    if stream.path != None:
        props['defaultFile'] = stream.path

    props['wildcard'] = '|'.join([
            _('All supported files'), subtitleWildcard + ';' + videoWildcard,
            _('Subtitle files'), subtitleWildcard,
            _('Video files'), videoWildcard,
            _('All files'), '*.*' ])

    path = showOpenFileDlg(parent, **props)
    if path != None:
        return Stream(path=path, types=stream.types)


class OpenWin(gui.openwin_layout.OpenWin):
    def __init__(self, parent, stream):
        gui.openwin_layout.OpenWin.__init__(self, parent)
        setFileDropTarget(self, self.onDropFile)
        self.stream = Stream(stream=stream)
        self.openStream(stream)

    @error_dlg
    def openStream(self, stream=None, path=None):
        if path:
            stream = Stream(path=path, types=self.stream.types)

        self.stream = stream
        self.m_textPath.SetValue(self.stream.path)
        self.m_textPath.SetInsertionPoint(self.m_textPath.GetLastPosition())

        self.m_choiceEncoding.Enable(False)
        self.m_buttonOk.Enable(False)

        lang = stream.lang
        enc = stream.enc

        self.m_listStreams.setStreams(stream.streams, stream.types)

        if self.m_listStreams.GetItemCount() == 0:
            raise Error(_('There are no usable streams'),
                    path=stream.path,
                    types=self.stream.types)

        if stream.no != None:
            self.selectStream(stream.stream())

        self.m_choiceLang.setLang(lang)
        self.m_choiceEncoding.setCharEnc(enc)

    def selectStream(self, stream, updateLang=False):
        self.m_listStreams.selectStream(stream.no)
        self.stream.no = stream.no
        self.stream.type = stream.type

        if updateLang and stream.lang:
            self.stream.lang = stream.lang
            self.m_choiceLang.setLang(stream.lang)

        self.m_choiceEncoding.Enable(stream.type == 'subtitle/text')
        self.m_buttonOk.Enable(True)

    def onChoiceLangChoice(self, event):
        self.stream.lang = self.m_choiceLang.getLang()

    def onListStreamsSelect(self, event):
        index = self.m_listStreams.getSelectedStream()
        if index != None:
            self.selectStream(self.stream.streams[index], updateLang=True)

    def onListStreamsDClick(self, event):
        self.EndModal(wx.ID_OK)

    def onChoiceEncChoice(self, event):
        self.stream.enc = self.m_choiceEncoding.getCharEnc()

    @error_dlg
    def onButtonOpenClick(self, event):
        stream = showOpenSubFileDlg(self, self.stream)
        if stream != None and stream.isOpen():
            self.openStream(stream)

    def onDropFile(self, filename):
        self.openStream(path=filename)
        return True
