import wx


class BusyDlg(wx.Frame):
    def __init__(self, parent, msg):
        style = wx.BORDER_SIMPLE | wx.FRAME_TOOL_WINDOW
        if parent:
            style |= wx.FRAME_FLOAT_ON_PARENT

        super().__init__(parent, style=style)

        self.disabler = None
        panel = wx.Panel(self)
        text = wx.StaticText(panel, label=msg)

        fgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        bgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        for win in [panel, text]:
            win.SetCursor(wx.HOURGLASS_CURSOR)
            win.SetForegroundColour(fgColor)
            win.SetBackgroundColour(bgColor)

        size = text.GetBestSize()
        self.SetClientSize((size.width + 80, size.height + 40))
        panel.SetSize(self.GetClientSize())
        text.Center()
        self.Center()

    def __enter__(self):
        self.disabler = wx.WindowDisabler(self)
        self.Show()
        self.Refresh()
        self.Update()
        wx.Yield()

    def __exit__(self, type, value, traceback):
        self.Close()

        if self.disabler:
            del self.disabler
            self.disabler = None

