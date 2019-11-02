import subsync.gui.layout.streamselwin
from subsync.data import languages
import wx
import os

import logging
logger = logging.getLogger(__name__)


class StreamSelectionWin(subsync.gui.layout.streamselwin.StreamSelectionWin):
    def __init__(self, parent, streams, types):
        super().__init__(parent)

        self.streams = streams
        self.selection = []

        self.m_items.SetIconMap({
            False: wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_MENU),
            True:  wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_MENU)
        })

        for s in streams:
            self.m_items.InsertItem(os.path.basename(s.path), icon=False)

        self.m_choiceSelType.SetClientData(0, ['subtitle/text', 'audio'])
        self.m_choiceSelType.SetClientData(1, ['subtitle/text'])
        self.m_choiceSelType.SetClientData(2, ['audio'])

        stypes = set(s.type for ss in streams for s in ss.streams.values()) & set(types)
        hasAudio = 'audio' in stypes
        hasSubtitle = 'subtitle/text' in stypes

        enableTypeSelection = hasAudio and hasSubtitle
        self.m_textSelType.Show(enableTypeSelection)
        self.m_choiceSelType.Show(enableTypeSelection)

        langs = set(canonizeLang(s.lang) for ss in streams for s in ss.streams.values() if s.type in types)
        self.m_choiceSelLang.Append(_('auto'), None)
        if '' in langs:
            langs.discard('')
            self.m_choiceSelLang.Append(_('<undefined>'), '')

        self.m_choiceSelLang.addSortedLangs({ languages.getName(l): l for l in langs })
        self.m_choiceSelLang.SetSelection(0)

        titles = set(s.title for ss in streams for s in ss.streams.values() if s.type in types)
        self.m_choiceSelTitle.Append(_('auto'), None)
        for title in sorted(titles):
            value = title
            if title == '':
                title = _('<empty>')
            self.m_choiceSelTitle.Append(title, value)
        self.m_choiceSelTitle.SetSelection(0)

        self.m_textSelTitle.Show(len(titles) > 1)
        self.m_choiceSelTitle.Show(len(titles) > 1)

        self.onSelChange()

        self.Fit()
        self.Layout()

    def getSelection(self):
        return self.selection

    def onSelChange(self, event=None):
        types = self.getSelType()
        title = self.getSelTitle()
        lang = self.m_choiceSelLang.GetValue()

        self.selection = [ findStream(s, types, lang, title) for s in self.streams ]
        for no, sel in enumerate(self.selection):
            self.m_items.SetIcon(no=no, icon=sel is not None)

    def getSelType(self):
        i = self.m_choiceSelType.GetSelection()
        if i != wx.NOT_FOUND:
            return self.m_choiceSelType.GetClientData(i)

    def getSelTitle(self):
        i = self.m_choiceSelTitle.GetSelection()
        if i != wx.NOT_FOUND:
            return self.m_choiceSelTitle.GetClientData(i)


def findStream(ss, types, lang, title):
    items = sorted(ss.streams.items())
    streams = []
    for type in types:
        # we will try streams that have lang set first
        streams += [ (no, s) for no, s in items if s.type == type and canonizeLang(s.lang) ]
        streams += [ (no, s) for no, s in items if s.type == type and not canonizeLang(s.lang) ]

    if lang is not None:
        streams = [ ss for ss in streams if canonizeLang(ss[1].lang) == lang ]

    if title is not None:
        streams = [ ss for ss in streams if ss[1].title == title ]

    if streams:
        return streams[0][0]


def canonizeLang(lang):
    lang = lang.lower()
    if lang != 'und':
        return lang
    return ''
