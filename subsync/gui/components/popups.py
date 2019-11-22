import wx
from subsync.settings import settings


class PopupInfoButton(wx.BitmapButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.onClick)
        self.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_BUTTON))
        self.message = None

    def onClick(self, event):
        if self.message:
            parent = self.GetParent()
            caption = self.GetLabel() or _('Info')
            with wx.MessageDialog(parent, self.message, caption) as dlg:
                dlg.ShowModal()


def showConfirmationPopup(parent, msg, title, confirmKey=None):
    if confirmKey and not settings().get(confirmKey):
        return True

    with wx.RichMessageDialog(parent, msg, title, wx.YES_NO | wx.ICON_QUESTION) as dlg:
        if confirmKey:
            dlg.ShowCheckBox(_('don\'t show this message again'))
        res = dlg.ShowModal() == wx.ID_YES

        if res and confirmKey and dlg.IsCheckBoxChecked():
            settings().setValue(confirmKey, False)
            settings().save()

        return res
