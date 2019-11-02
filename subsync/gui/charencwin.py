import wx
from subsync.data import charenc


class CharactersEncodingWin(wx.SingleChoiceDialog):
    def __init__(self, parent):
        self.encs = [ None ]
        names = [ _('<auto>') ]

        for code, name in charenc.charEncodings:
            self.encs.append(code)
            names.append('{} - {}'.format(code, name))

        msg = _('Select character encoding')
        super().__init__(parent, msg, _('Character encoding'), names)

    def SetValue(self, enc):
        try:
            no = self.encs.index(enc)
            self.SetSelection(no)
        except:
            pass

    def GetValue(self):
        sel = self.GetSelection()
        if sel == wx.NOT_FOUND:
            return wx.NOT_FOUND
        else:
            return self.encs[sel]
