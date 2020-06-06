import subsync.gui.layout.openwin
import wx
from subsync.synchro import ChannelsMap
from subsync.gui.components import filedlg
from subsync.gui.components import filedrop
from subsync.gui import channelswin
from subsync.gui.busydlg import showBusyDlgAsyncJob
from subsync.gui.errorwin import error_dlg
from subsync.error import Error
from subsync.data.filetypes import subtitleWildcard, videoWildcard
from subsync.data import languages
from copy import copy


@error_dlg
def showOpenFileDlg(parent, file):
    props = {}
    if file.path != None:
        props['defaultFile'] = file.path

    props['wildcard'] = '|'.join([
            _('All supported files'), subtitleWildcard + ';' + videoWildcard,
            _('Subtitle files'), subtitleWildcard,
            _('Video files'), videoWildcard,
            _('All files'), '*.*' ])

    path = filedlg.showOpenFileDlg(parent, **props)
    if path:
        return readStream(parent, file, path)


def readStream(parent, file, path):
    msg = _('Loading, please wait...')
    f = copy(file)
    showBusyDlgAsyncJob(parent, msg, f.open, path=path)
    return f


class OpenWin(subsync.gui.layout.openwin.OpenWin):
    def __init__(self, parent, file, allowOpen=True, defaultLang=None):
        super().__init__(parent)
        self.defaultLang = defaultLang
        self.file = copy(file)
        self.openStream(self.file)

        self.m_buttonOpen.Show(allowOpen)
        if allowOpen:
            filedrop.setFileDropTarget(self, OnDropFile=self.onDropFile)

        self.Fit()
        self.Layout()

    @error_dlg
    def openStream(self, file=None, path=None):
        if path:
            file = readStream(self, self.file, path)

        self.file = file
        self.m_textPath.SetValue(self.file.path)
        self.m_textPath.SetInsertionPoint(self.m_textPath.GetLastPosition())

        self.m_choiceEncoding.Enable(False)
        self.m_buttonOk.Enable(False)

        lang = validateLang(file.lang)
        enc = file.enc
        channels = file.channels

        self.m_listStreams.setStreams(file.streams, file.types)

        if self.m_listStreams.GetItemCount() == 0:
            raise Error(_('There are no usable streams'),
                    path=file.path,
                    types=self.file.types)

        if file.no is not None:
            self.selectStream(file.stream())

        if not lang:
            lang = self.defaultLang

        file.lang = lang
        self.m_choiceLang.SetValue(lang)
        self.m_choiceEncoding.SetValue(enc)
        if channels:
            self.selectAudioChannels(channels)

    def selectStream(self, file, updateLang=False):
        self.m_listStreams.selectStream(file.no)
        self.file.no = file.no
        self.file.type = file.type

        if updateLang and file.lang:
            lang = validateLang(file.lang)
            if not lang:
                lang = self.defaultLang
            self.file.lang = lang
            self.m_choiceLang.SetValue(self.file.lang)

        isSubText = file.type == 'subtitle/text'
        isAudio = file.type == 'audio'

        if isAudio:
            self.selectAudioChannels(ChannelsMap.auto())
        else:
            self.m_textChannels.SetValue('')

        self.m_choiceEncoding.Enable(isSubText)
        self.m_textChannels.Enable(isAudio)
        self.m_buttonSelectChannels.Enable(isAudio)
        self.m_buttonOk.Enable(True)

    def selectAudioChannels(self, channels):
        self.file.channels = channels
        self.m_textChannels.SetValue(channels.getDescription())

    def onChoiceLangChoice(self, event):
        lang = validateLang(self.m_choiceLang.GetValue())
        self.file.lang = lang
        self.defaultLang = lang

    def onListStreamsSelect(self, event):
        index = self.m_listStreams.getSelectedStream()
        if index != None:
            self.selectStream(self.file.streams[index], updateLang=True)

    def onListStreamsDClick(self, event):
        self.EndModal(wx.ID_OK)

    def onChoiceEncChoice(self, event):
        self.file.enc = self.m_choiceEncoding.GetValue()

    @error_dlg
    def onButtonSelectChannelsClick(self, event):
        dlg = channelswin.ChannelsWin(self, self.file.stream().audio)
        dlg.SetValue(self.file.channels)
        if dlg.ShowModal() == wx.ID_OK:
            channels = dlg.GetValue()
            self.selectAudioChannels(channels)

    @error_dlg
    def onButtonOpenClick(self, event):
        file = showOpenFileDlg(self, self.file)
        if file != None and file.isOpen():
            self.openStream(file)

    def onDropFile(self, x, y, filename):
        self.openStream(path=filename)
        return True


def validateLang(lang):
    if lang and lang.lower() in languages.codes3:
        return lang.lower()
