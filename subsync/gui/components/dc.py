import wx

class BitmapMemoryDC(wx.MemoryDC):
    def __init__(self, width, height, fg=None, bg=None, highlighted=False):
        super().__init__()
        self.bmp = wx.Bitmap(width, height)
        self.SelectObject(self.bmp)

        if fg == None:
            if highlighted:
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
            else:
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        if bg == None:
            if highlighted:
                bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
            else:
                bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

        self.SetBrush(wx.Brush(fg))
        self.SetBackground(wx.Brush(bg))
        self.SetTextForeground(fg)
        self.SetTextBackground(bg)
        self.Clear()

    def getBitmap(self):
        self.SelectObject(wx.NullBitmap)
        return self.bmp

    def setFont(self, pointSize,
            family=wx.FONTFAMILY_DEFAULT,
            style=wx.FONTSTYLE_NORMAL,
            weight=wx.FONTWEIGHT_NORMAL):
        self.SetFont(wx.Font(pointSize, family, style, weight))

    def drawTextLimited(self, text, x, y, maxWidth):
        text, size = self.limitText(text, maxWidth)
        self.DrawText(text, x, y)
        return size

    def limitText(self, text, maxWidth, append='...'):
        size = self.GetTextExtent(text)
        if size.Width <= maxWidth:
            return text, size

        low = 0
        high = len(text) - 1

        i = 0
        while low <= high:
            i += 1
            mid = (high + low) // 2
            t = text[0:mid] + '...'
            size = self.GetTextExtent(t)

            if mid == low:
                break

            if size.Width < maxWidth:
                low = mid
            elif size.Width > maxWidth:
                high = mid
            else:
                break

        return t, size
