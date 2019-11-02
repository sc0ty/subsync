import subsync.gui.layout.batchlistitem
import wx


class BaseCell(subsync.gui.layout.batchlistitem.BatchListItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selected = None
        self.visible = False

    def objects(self):
        yield self
        for obj in self.GetChildren():
            yield obj

    def select(self, selected=True):
        selected = selected and self.visible
        if selected != self.selected:
            self.selected = selected
            if selected:
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
                bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
            else:
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
                bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            for obj in self.objects():
                obj.SetBackgroundColour(bg)
                obj.SetForegroundColour(fg)
            self.parent.updateEvent.emit()
            return self.visible

    def show(self, show=True):
        self.visible = show
        self.m_bitmapIcon.Show(show)
        self.m_textName.Show(show)
        self.m_textDetails.Show(show)
        self.parent.updateEvent.emit()

    def setInteractive(self):
        for obj in self.objects():
            obj.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
            obj.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
            obj.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDClick)

    def onLeftDown(self, event):
        if self.visible:
            if event.ControlDown():
                self.select(not self.selected)
            elif event.ShiftDown():
                coords = self.parent.getCellCoords(self)
                if coords:
                    self.parent.selectRange(coords[1], coords[0], clearOther=True)
            elif event.GetId() == self.m_bitmapIcon.GetId():
                self.select(not self.selected)
            elif not self.selected:
                self.parent.clearSelection(exclude=[ self ])
                self.select(True)
            if not event.ShiftDown():
                self.parent.setPickedCell(self)
        else:
            self.parent.clearSelection()
        event.Skip()

    def onLeftUp(self, event):
        if self.visible and not event.ControlDown() and not event.ShiftDown() \
                    and not event.GetId() == self.m_bitmapIcon.GetId():
                self.parent.clearSelection(exclude=[ self ])
                self.select(True)
                self.parent.setPickedCell(self)
        event.Skip()

    def onLeftDClick(self, event):
        event.Skip()
