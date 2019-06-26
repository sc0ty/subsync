import wx
from subsync import img


class PopupInfoButton(wx.BitmapButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.onClick)
        img.setItemBitmap(self, 'info')
        self.message = None

    def onClick(self, event):
        if self.message:
            parent = self.GetParent()
            caption = self.GetLabel()
            with wx.MessageDialog(parent, self.message, caption) as dlg:
                dlg.ShowModal()
