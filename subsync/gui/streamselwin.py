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

        self.onSelChange()

        self.Fit()
        self.Layout()

    def getSelection(self):
        return self.selection

    def onSelChange(self, event=None):
        types = self.getSelType()
        lang = self.m_choiceSelLang.GetValue()

        self.selection = [ findStream(s, types, lang) for s in self.streams ]
        for no, sel in enumerate(self.selection):
            self.m_items.SetIcon(no=no, icon=bool(sel))

    def getSelType(self):
        i = self.m_choiceSelType.GetSelection()
        if i != wx.NOT_FOUND:
            return self.m_choiceSelType.GetClientData(i)


def findStream(ss, types, lang):
    items = sorted(ss.streams.items())
    streams = []
    for type in types:
        streams += [ (no, s) for no, s in items if s.type == type and s.lang ]
        streams += [ (no, s) for no, s in items if s.type == type and not s.lang ]

    if streams:
        if lang:
            for no, stream in streams:
                if stream.lang.lower() == lang:
                    return no
        else:
            return streams[0][0]
