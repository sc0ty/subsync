import subsync.gui.layout.streamselwin
from subsync import img
from subsync.utils import getLanguageName
import wx
import os

import logging
logger = logging.getLogger(__name__)


class StreamSelectionWin(subsync.gui.layout.streamselwin.StreamSelectionWin):
    def __init__(self, parent, streams, types):
        super().__init__(parent)

        img.setItemBitmap(self.m_bitmapTick, 'tickmark')
        img.setItemBitmap(self.m_bitmapCross, 'crossmark')

        self.streams = streams
        self.selection = []

        self.m_items.SetIconMap({
            False: img.getBitmap('crossmark'),
            True:  img.getBitmap('tickmark')
        })

        for s in streams:
            self.m_items.InsertItem(os.path.basename(s.path), icon=False)

        self.m_choiceSelType.SetClientData(0, ['subtitle/text', 'audio'])
        self.m_choiceSelType.SetClientData(1, ['subtitle/text'])
        self.m_choiceSelType.SetClientData(2, ['audio'])

        types = set(s.type for ss in streams for s in ss.streams.values()) & set(types)
        hasAudio = 'audio' in types
        hasSubtitle = 'subtitle/text' in types

        enableTypeSelection = hasAudio and hasSubtitle
        self.m_textSelType.Show(enableTypeSelection)
        self.m_choiceSelType.Show(enableTypeSelection)

        langs = set(s.lang.lower() for ss in streams for s in ss.streams.values())
        self.m_choiceSelLang.Append(_('auto'), None)
        if langs & set(['', 'und']):
            langs.discard('')
            langs.discard('und')
            self.m_choiceSelLang.Append(_('<undefined>'), '')

        self.m_choiceSelLang.addSortedLangs({getLanguageName(l): l for l in langs})
        self.m_choiceSelLang.SetSelection(0)

        titles = set(s.title for ss in streams for s in ss.streams.values())
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
        streams += [ (no, s) for no, s in items if s.type == type and s.lang ]
        streams += [ (no, s) for no, s in items if s.type == type and not s.lang ]

    if lang is not None:
        streams = [ ss for ss in streams if ss[1].lang.lower() == lang ]

    if title is not None:
        streams = [ ss for ss in streams if ss[1].title == title ]

    if streams:
        return streams[0][0]
