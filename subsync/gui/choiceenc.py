import wx
from subsync.data.charenc import charEncodings


class ChoiceCharEnc(wx.Choice):
    def __init__(self, *args, **kwargs):
        wx.Choice.__init__(self, *args, **kwargs)
        self.Append(_('Auto detect'), None)
        for enc in charEncodings:
            name = '{} - {}'.format(enc[0], enc[1])
            self.Append(name, enc[0])

    def SetValue(self, enc):
        if enc != None:
            for i in range(1, self.GetCount()):
                if self.GetClientData(i).lower() == enc.lower():
                    self.SetSelection(i)
                    return
        self.SetSelection(0)

    def GetValue(self):
        i = self.GetSelection()
        return self.GetClientData(i) if i != -1 else None

