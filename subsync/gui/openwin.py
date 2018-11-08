import gui.openwin_layout
import wx
from stream import Stream
from speech import getDefaultAudioChannels
from gui.filedlg import showOpenFileDlg
from gui.filedrop import setFileDropTarget
from gui.channelssel import AudioChannelsSel
from gui.errorwin import error_dlg
from error import Error
from data.filetypes import subtitleWildcard, videoWildcard
from data.languages import languages2to3


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

        if not stream.lang and len(stream.streams) == 1:
            stream.lang = getLangFromPath(stream.path)
            print(stream.lang)

        lang = stream.lang
        enc = stream.enc
        channels = stream.channels

        self.m_listStreams.setStreams(stream.streams, stream.types)

        if self.m_listStreams.GetItemCount() == 0:
            raise Error(_('There are no usable streams'),
                    path=stream.path,
                    types=self.stream.types)

        if stream.no != None:
            self.selectStream(stream.stream())

        self.m_choiceLang.setLang(lang)
        self.m_choiceEncoding.setCharEnc(enc)
        if channels:
            self.selectAudioChannels(channels)

    def selectStream(self, stream, updateLang=False):
        self.m_listStreams.selectStream(stream.no)
        self.stream.no = stream.no
        self.stream.type = stream.type

        if updateLang and stream.lang:
            self.stream.lang = stream.lang
            self.m_choiceLang.setLang(stream.lang)

        isSubText = stream.type == 'subtitle/text'
        isAudio = stream.type == 'audio'

        if isAudio:
            self.selectAudioChannels(getDefaultAudioChannels(stream.audio))
        else:
            self.selectAudioChannels(None)

        self.m_choiceEncoding.Enable(isSubText)
        self.m_textChannels.Enable(isAudio)
        self.m_buttonSelectChannels.Enable(isAudio)
        self.m_buttonOk.Enable(True)

    def selectAudioChannels(self, channels):
        self.stream.channels = channels

        if channels:
            names = self.stream.stream().audio.getChannelNames()
            if len(channels) == len(names):
                self.m_textChannels.SetValue(_('all channels'))
            else:
                chls = [ names[id] for id in channels ]
                self.m_textChannels.SetValue(', '.join(chls))

        else:
            self.m_textChannels.SetValue('')

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
    def onButtonSelectChannelsClick(self, event):
        dlg = AudioChannelsSel(self,
                _('Select audio channels to listen:'),
                _('Select channels'),
                self.stream.stream().audio)

        dlg.selectChannels(self.stream.channels)
        if dlg.ShowModal() == wx.ID_OK:
            channels = dlg.getSelectedChannels()
            if len(channels) == 0:
                raise Error(_('At lest one audio channel must be selected'))
            self.selectAudioChannels(channels)

    @error_dlg
    def onButtonOpenClick(self, event):
        stream = showOpenSubFileDlg(self, self.stream)
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

