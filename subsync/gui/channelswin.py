import wx
import gui.channelswin_layout
import utils
import gizmo


def getChannelDescription(ch):
    name = gizmo.AudioFormat.getChannelName(ch)
    desc = gizmo.AudioFormat.getChannelDescription(ch)
    if name and desc:
        return '{} ({})'.format(desc, name)
    else:
        return 'channel {}'.format(ch)


def getChannelName(ch):
    return gizmo.AudioFormat.getChannelName(ch) or 'CH{}'.format(ch)


def getChannelNames(chs):
    if not chs:
        return _('auto')
    elif chs == 'all':
        return _('all channels')
    else:
        return ', '.join([ getChannelName(ch) for ch in chs ])


class ChannelsWin(gui.channelswin_layout.ChannelsWin):
    def __init__(self, parent, audio):
        super().__init__(parent)

        self.channels = {}
        for channel in utils.splitBitVector(audio.channelLayout):
            self.addChannel(channel)

        self.Fit()
        self.Layout()

    def addChannel(self, channel):
        name = getChannelDescription(channel)
        box = wx.CheckBox(self.m_panelCustom, wx.ID_ANY, name)
        self.m_panelCustom.GetSizer().Add(box, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        self.channels[channel] = box
        self.m_radioCustom.Enable(True)

    def onRadioButtonToggle(self, event):
        custom = self.m_radioCustom.GetValue()
        self.m_panelCustom.Enable(custom)

    def SetValue(self, channels):
        if not channels:
            self.m_radioAuto.SetValue(True)
            self.m_panelCustom.Enable(False)

        elif channels == 'all':
            self.m_radioAllChannels.SetValue(True)
            self.m_panelCustom.Enable(False)

        else:
            self.m_radioCustom.SetValue(True)
            self.m_panelCustom.Enable(True)

            enabled  = [ ch for ch in channels if ch in self.channels ]
            disabled = [ ch for ch in set(self.channels) - set(channels) ]

            for ch in enabled:
                self.channels[ch].SetValue(True)

            for ch in disabled:
                self.channels[ch].SetValue(False)

    def GetValue(self):
        if self.m_radioAuto.GetValue():
            return None
        elif self.m_radioAllChannels.GetValue():
            return 'all'
        else:
            return [ ch for ch in self.channels if self.channels[ch].GetValue() ]

