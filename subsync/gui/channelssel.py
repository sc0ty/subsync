import wx
import utils
import gizmo


def channelName(ch):
    if ch:
        return gizmo.AudioFormat.getChannelDescription(ch) or str(ch)
    else:
        return _('auto')


def channelNames(chs):
    if chs:
        return ', '.join([ gizmo.AudioFormat.getChannelName(ch) or str(ch)
            for ch in chs ])
    else:
        return channelName(0)


class AudioChannelsSel(wx.MultiChoiceDialog):
    def __init__(self, parent, msg, caption, audio):
        self.ids = [ 0 ] + utils.splitBitVector(audio.channelLayout)
        names = [ channelName(ch) for ch in self.ids ]
        super().__init__(parent, msg, caption, names)
        self.selectChannels(None)

    def selectChannels(self, channels):
        if channels:
            sel = [ self.ids.index(ch) for ch in channels if ch in self.ids ]
            self.SetSelections(sel)
        else:
            self.SetSelections([ 0 ])

    def getSelectedChannels(self):
        sel = self.GetSelections()
        if 0 not in sel and len(sel) > 0:
            return [ self.ids[ch] for ch in sel ]

