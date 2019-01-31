import subsync.gui.layout.openwin
import wx
from subsync.stream import Stream
from subsync import channels
from subsync.gui import filedlg
from subsync.gui import filedrop
from subsync.gui import channelswin
from subsync.gui import busydlg
from subsync.gui.errorwin import error_dlg
from subsync.error import Error
from subsync.data.filetypes import subtitleWildcard, videoWildcard
from subsync.data.languages import languages, languages2to3


@error_dlg
def showOpenFileDlg(parent, stream):
    props = {}
    if stream.path != None:
        props['defaultFile'] = stream.path

    props['wildcard'] = '|'.join([
            _('All supported files'), subtitleWildcard + ';' + videoWildcard,
            _('Subtitle files'), subtitleWildcard,
            _('Video files'), videoWildcard,
            _('All files'), '*.*' ])

    path = filedlg.showOpenFileDlg(parent, **props)
    return readStream(parent, path, stream.types)


def readStream(parent, path, types):
    if path:
        with busydlg.BusyDlg(parent, _('Loading, please wait...')):
            return Stream(path=path, types=types)


class OpenWin(subsync.gui.layout.openwin.OpenWin):
    def __init__(self, parent, stream):
        super().__init__(parent)
        filedrop.setFileDropTarget(self, self.onDropFile)
        self.stream = Stream(stream=stream)
        self.openStream(stream)

    @error_dlg
    def openStream(self, stream=None, path=None):
        if path:
            return readStream(self, path, self.stream.types)

        self.stream = stream
        self.m_textPath.SetValue(self.stream.path)
        self.m_textPath.SetInsertionPoint(self.m_textPath.GetLastPosition())

        self.m_choiceEncoding.Enable(False)
        self.m_buttonOk.Enable(False)

        if not stream.lang and len(stream.streams) == 1:
            stream.lang = validateLang(getLangFromPath(stream.path))

        lang = validateLang(stream.lang)
        enc = stream.enc
        channels = stream.channels

        self.m_listStreams.setStreams(stream.streams, stream.types)

        if self.m_listStreams.GetItemCount() == 0:
            raise Error(_('There are no usable streams'),
                    path=stream.path,
                    types=self.stream.types)

        if stream.no != None:
            self.selectStream(stream.stream())

        stream.lang = lang
        self.m_choiceLang.SetValue(lang)
        self.m_choiceEncoding.SetValue(enc)
        if channels:
            self.selectAudioChannels(channels)

    def selectStream(self, stream, updateLang=False):
        self.m_listStreams.selectStream(stream.no)
        self.stream.no = stream.no
        self.stream.type = stream.type

        if updateLang and stream.lang:
            self.stream.lang = validateLang(stream.lang)
            self.m_choiceLang.SetValue(self.stream.lang)

        isSubText = stream.type == 'subtitle/text'
        isAudio = stream.type == 'audio'

        if isAudio:
            self.selectAudioChannels(channels.AutoChannelsMap())
        else:
            self.m_textChannels.SetValue('')

        self.m_choiceEncoding.Enable(isSubText)
        self.m_textChannels.Enable(isAudio)
        self.m_buttonSelectChannels.Enable(isAudio)
        self.m_buttonOk.Enable(True)

    def selectAudioChannels(self, channels):
        self.stream.channels = channels
        self.m_textChannels.SetValue(channels.getDescription())

    def onChoiceLangChoice(self, event):
        self.stream.lang = validateLang(self.m_choiceLang.GetValue())

    def onListStreamsSelect(self, event):
        index = self.m_listStreams.getSelectedStream()
        if index != None:
            self.selectStream(self.stream.streams[index], updateLang=True)

    def onListStreamsDClick(self, event):
        self.EndModal(wx.ID_OK)

    def onChoiceEncChoice(self, event):
        self.stream.enc = self.m_choiceEncoding.GetValue()

    @error_dlg
    def onButtonSelectChannelsClick(self, event):
        dlg = channelswin.ChannelsWin(self, self.stream.stream().audio)
        dlg.SetValue(self.stream.channels)
        if dlg.ShowModal() == wx.ID_OK:
            channels = dlg.GetValue()
            self.selectAudioChannels(channels)

    @error_dlg
    def onButtonOpenClick(self, event):
        stream = showOpenFileDlg(self, self.stream)
        if stream != None and stream.isOpen():
            self.openStream(stream)

    def onDropFile(self, filename):
        self.openStream(path=filename)
        return True


def getLangFromPath(path):
    ''' Returns two- or three-letters language code from filename in form
    name.code.extension, e.g. subtitles.eng.srt or subtitles-fr.srt
    '''

    name = path.rsplit('.', 1)[0]
    size = 0

    for c in reversed(name):
        if c.isalpha():
            size += 1
        else:
            break

    if size == 2:
        return languages2to3.get(name[-2:].lower())
    elif size == 3:
        return name[-3:].lower()


def validateLang(lang):
    if lang and lang.lower() in languages:
        return lang.lower()

