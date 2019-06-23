import wx
from subsync.gui.components import filedrop


class MultiColumnCol(object):
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, key):
        return self.items[key]

    def __bool__(self):
        return True

    def canAddFiles(self, index):
        return False

    def addFiles(self, paths, index):
        return []

    def canAddItems(self, items, index):
        return []

    def addItems(self, items, index):
        i = self.canAddItems(items, index)
        self.items[index:index] = i
        return i

    def removeItems(self, items):
        for item in items:
            if item in self.items:
                self.items.remove(item)

    def getItemBitmap(self, index, width, height, selected):
        return wx.NullBitmap

    def getContextMenu(self, parent, item):
        return None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.items)


class MultiColumnView(wx.ScrolledWindow):
    def __init__(self, parent, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, parent, *args, **kwargs)

        self.AlwaysShowScrollbars(vflag=True, hflag=False)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)
        self.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenuShow)

        self.itemHeight = 0

        self.cols = []
        self.colWidth = 0

        self.selectedItems = set()
        self.markedRow = 0

        self.dragSource = None
        self.dragPos = None
        self.drawDragPos = False

        self.onItemsChange = lambda: None
        self.onSelection = lambda: None

        filedrop.setFileDropTarget(
                self,
                OnDropFiles=self.onFilesDrop,
                OnDragOver=self.onFilesDrag,
                OnLeave=self.onFilesDragLeave,
                children=False)

    def __len__(self):
        return min(len(col) for col in self.cols)

    def __iter__(self):
        for row in zip(*self.cols):
            yield row

    def __getitem__(self, key):
        return [ col[key] for col in self.cols ]

    def addCol(self, col, itemHeight=0):
        self.itemHeight = max(self.itemHeight, itemHeight)
        self.cols.append(col)
        self.onResize(None)

    def addFiles(self, col, paths, index=None):
        if index == None:
            index = len(col)

        added = col.addFiles(paths, index)
        if added:
            self.updateSize()
            self.selectedItems = set(added)
            self.markedRow = index

            self.onItemsChange()
            self.Refresh()
        return added

    def removeItems(self, items, keepSelection=False):
        for col in self.cols:
            col.removeItems(items)

        if not keepSelection:
            self.setSelection(self.selectedItems - set(items))

        self.onItemsChange()
        self.updateSize()

    def getColAt(self, pos):
        posX = int(pos[0] / self.colWidth)
        if posX >= 0 and posX < len(self.cols):
            return self.cols[posX]

    def getItemAt(self, pos):
        col = self.getColAt(pos)
        if col:
            index = self.getItemIndex(pos, col)
            if index < len(col):
                return col[index], col, index
            return None, col, 0
        return None, None, 0

    def getItemIndex(self, pos, col=None):
        index = int(pos[1] / self.itemHeight)
        if col:
            index = min(index, len(col))
        return index

    def getDragItemIndex(self, pos, col=None):
        index = max(round(pos[1] / self.itemHeight), 0)
        if col:
            index = min(index, len(col))
        return index

    def clearSelection(self):
        self.selectedItems = set()
        self.onSelection()

    def setSelection(self, items):
        self.selectedItems = set(items)
        self.onSelection()

    def getSelection(self):
        return self.selectedItems

    def getSelectionInCol(self, col):
        return [ item for item in col if item in self.selectedItems ]

    def updateSize(self):
        size = self.GetClientSize()
        size.SetHeight(self.itemHeight * max([ len(col) for col in self.cols ]))
        self.SetVirtualSize(size)

    def onMouseLeftDown(self, event):
        if not event.ControlDown() and not event.ShiftDown():
            pos = self.CalcUnscrolledPosition(event.GetPosition())
            item, col, index = self.getItemAt(pos)
            if item and not item in self.selectedItems:
                self.setSelection([item])
                self.markedRow = index
                self.Refresh()

    def onMouseLeftUp(self, event):
        pos = self.CalcUnscrolledPosition(event.GetPosition())

        if self.dragPos or self.dragSource:
            self.dragPos = None
            self.dragSource = None

        else:
            item, col, index = self.getItemAt(pos)
            if item:
                if event.ControlDown():
                    selectedItems = self.selectedItems & set(self.getColAt(pos))
                    if item in selectedItems:
                        selectedItems.remove(item)
                    else:
                        selectedItems.add(item)
                        self.markedRow = index
                    self.setSelection(selectedItems)

                elif event.ShiftDown():
                    first = min(index, self.markedRow)
                    last  = max(index, self.markedRow) + 1
                    self.setSelection(col[first:last])

                else:
                    self.setSelection([item])
                    self.markedRow = index
            else:
                self.clearSelection()
            self.Refresh()

    def onMouseMove(self, event):
        if event.Dragging() and not event.ControlDown() and not event.ShiftDown():
            pos = self.CalcUnscrolledPosition(event.GetPosition())
            col = self.getColAt(pos)
            index = self.getDragItemIndex(pos, col)
            if col:
                dragPos = (int(pos[0] / self.colWidth), index)
                if dragPos != self.dragPos:
                    if self.dragPos and self.dragSource:
                        srcItems = [ item for item in self.dragSource if item in self.selectedItems ]
                        dstItems = col.canAddItems(srcItems, index)
                        if dstItems:
                            self.removeItems(dstItems, keepSelection=True)
                            col.addItems(dstItems, index)

                            if self.dragSource != col:
                                self.setSelection(self.selectedItems & set(col))

                            self.onItemsChange()
                            self.updateSize()
                            self.Refresh()

                    self.dragPos = dragPos
                    self.dragSource = col

    def onFilesDrop(self, x, y, paths):
        pos = self.CalcUnscrolledPosition(x, y)
        col = self.getColAt(pos)
        index = self.getDragItemIndex(pos, col)
        if col:
            addedItems = self.addFiles(col, paths, index)
            if addedItems:
                self.drawDragPos = False
                self.dragPos = None

                self.updateSize()
                self.setSelection(addedItems)

                self.onItemsChange()
                self.Refresh()
                return True
        return False

    def onFilesDrag(self, x, y, result):
        pos = self.CalcUnscrolledPosition(x, y)
        col = self.getColAt(pos)
        index = self.getDragItemIndex(pos, col)
        if col and col.canAddFiles(pos):
            dragPos = (int(pos[0] / self.colWidth), index)
            if self.dragPos != dragPos:
                self.drawDragPos = True
                self.dragPos = dragPos
                self.Refresh()
        else:
            self.drawDragPos = False
            self.dragPos = None
            self.Refresh()
        return result

    def onFilesDragLeave(self):
        if self.dragPos or self.drawDragPos:
            self.drawDragPos = False
            self.dragPos = None
            self.Refresh()

    def onContextMenuShow(self, event):
        pos = self.CalcUnscrolledPosition(event.GetPosition() - self.GetScreenPosition())
        item, col, index = self.getItemAt(pos)
        if item and col:
            self.setSelection([item])
            self.markedRow = index
            self.Refresh()

            menu = col.getContextMenu(self, item)
            if menu:
                self.PopupMenu(menu)

    def onResize(self, event):
        virtual = self.GetVirtualSize()
        client = self.GetClientSize()
        if virtual.width > client.Width:
            virtual.SetWidth(client.Width)
            self.SetVirtualSize(virtual)
        cols = len(self.cols) or 1
        self.colWidth = int(virtual.Width / cols)

    def onPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        client = self.GetClientSize()

        for colNo, col in enumerate(self.cols):
            x = colNo * self.colWidth

            for rowNo in range(len(col)):
                y = rowNo * self.itemHeight
                sx, sy = self.CalcScrolledPosition(x, y)

                if sy + self.itemHeight >= 0 and sy < client.Height:
                    selected = col[rowNo] in self.selectedItems
                    bmp = col.getItemBitmap(rowNo, self.colWidth, self.itemHeight, selected)
                    dc.DrawBitmap(bmp, sx, sy)

        if self.drawDragPos and self.dragPos:
            x1, y = self.dragPos
            x2 = x1 + 1
            dc.DrawLine(
                    self.CalcScrolledPosition(x1*self.colWidth, y*self.itemHeight),
                    self.CalcScrolledPosition(x2*self.colWidth, y*self.itemHeight))
