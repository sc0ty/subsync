import wx
import string


class ComboFps(wx.ComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fps in [ 10, 16, 23.976, 24, 25, 29.97, 30, 48, 50, 59.94, 60 ]:
            self.add(fps)

        self.Bind(wx.EVT_TEXT, self.onUpdate)
        self.lastValue = ''

    def add(self, fps):
        val = '{:.3f}'.format(fps)
        self.Append(val)

    def SetValue(self, fps):
        val = '{:.3f}'.format(fps)
        super().SetValue(val)

    def GetValue(self):
        try:
            return float(super().GetValue())
        except:
            return None

    def onUpdate(self, event):
        if self.isValid():
            self.lastValue = super().GetValue()
        else:
            super().SetValue(self.lastValue)

    def isValid(self):
        hasDot = False

        for ch in super().GetValue():
            if ch not in string.digits and ch != '.':
                return False

            if ch == '.':
                if hasDot:
                    return False
                hasDot = True

        return True

