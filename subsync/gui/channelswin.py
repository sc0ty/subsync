import wx
import subsync.gui.layout.channelswin
from subsync.synchro import ChannelsMap


class ChannelsWin(subsync.gui.layout.channelswin.ChannelsWin):
    def __init__(self, parent, audio):
        super().__init__(parent)

        self.channels = {}
        for channel in ChannelsMap.layoutToIds(audio.channelLayout):
            self.addChannel(channel)

        self.update()
        self.Fit()
        self.Layout()
        self.m_panelCustom.Enable(False)

    def addChannel(self, channel):
        name = ChannelsMap.getChannelDescription(channel)
        box = wx.CheckBox(self.m_panelCustom, wx.ID_ANY, name)
        self.m_panelCustom.GetSizer().Add(box, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        box.Bind(wx.EVT_CHECKBOX, self.onCheckCustomChannelCheck)

        self.channels[channel] = box
        self.m_radioCustom.Enable(True)

    def onRadioButtonToggle(self, event):
        custom = self.m_radioCustom.GetValue()
        self.m_panelCustom.Enable(custom)
        self.update()

    def onCheckCustomChannelCheck(self, event):
        self.update()

    def update(self):
        valid = self.isValid()
        enabled = self.m_buttonOK.IsEnabled()
        if valid ^ enabled:
            self.m_buttonOK.Enable(valid)

        if not self.m_radioCustom.GetValue():
            sel = self.GetValue().getLayoutMap(sum(self.channels))
            self.selectCustom(sel.channels)

    def selectCustom(self, sel):
        enabled  = [ ch for ch in sel if ch in self.channels ]
        disabled = [ ch for ch in set(self.channels) - set(sel) ]

        for ch in enabled:
            self.channels[ch].SetValue(True)

        for ch in disabled:
            self.channels[ch].SetValue(False)

    def isValid(self):
        if self.m_radioCustom.GetValue():
            for box in self.channels.values():
                if box.GetValue():
                    return True
            return False
        else:
            return True

    def SetValue(self, val):
        if val.type == 'auto':
            self.m_radioAuto.SetValue(True)
            self.m_panelCustom.Enable(False)

        elif val.type == 'all':
            self.m_radioAllChannels.SetValue(True)
            self.m_panelCustom.Enable(False)

        else:
            self.m_radioCustom.SetValue(True)
            self.m_panelCustom.Enable(True)
            self.selectCustom(val.channels)

        self.update()

    def GetValue(self):
        if self.isValid():
            if self.m_radioAuto.GetValue():
                return ChannelsMap.auto()
            elif self.m_radioAllChannels.GetValue():
                return ChannelsMap.all()
            else:
                chs = [ c for c in self.channels if self.channels[c].GetValue() ]
                return ChannelsMap.custom(chs)
        else:
            return ChannelsMap.auto()
