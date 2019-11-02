from .inputcell import DropPlaceholderItem
from subsync.synchro import SubFile, RefFile
from subsync.gui.components.update import updateLocker
from subsync.gui.components.notifier import DelayedSignalNotifier
import wx


class DropExternal(wx.FileDropTarget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.col = None
        self.row = None
        self.newItem = DropPlaceholderItem()
        self.delayedCancel = DelayedSignalNotifier(0.05, self.cancel)

    def move(self, row, col):
        if self.col != col or self.row != row:
            with updateLocker(self.parent):
                if self.col is not None:
                    self.parent.removeItem(self.row, self.col)
                    row = min(row, self.parent.GetItemCount())

                self.parent.insertItem(row, col, self.newItem, select=True)
                self.col = col
                self.row = row

    def apply(self, row, col, paths):
        with updateLocker(self.parent):
            if self.col is not None:
                self.parent.removeItem(self.row, self.col)
                row = min(row, self.parent.GetItemCount())

            # CallAfter because we don't wan't to block drop source
            wx.CallAfter(self.parent.addFiles, paths, row=row, col=col)

            self.col = None
            self.row = None

    def cancel(self):
        if self.col is not None:
            self.parent.removeItem(self.row, self.col)
        self.col = None
        self.row = None

    def OnDropFiles(self, x, y, paths):
        self.delayedCancel.clear()
        col = self.parent.getInputCol(x)
        if col is not None:
            row = self.parent.getRow(x, y)
            self.apply(row, col, paths)
            return True
        else:
            self.cancel()
            return False

    def OnDragOver(self, x, y, result):
        self.delayedCancel.clear()
        col = self.parent.getInputCol(x)
        if self.col is None:
            self.parent.clearSelection()
        if col is not None:
            maxRow = self.parent.GetItemCount() - int(col == self.col)
            row = min(self.parent.getRow(x, y), maxRow)
            self.move(row, col)
        return result

    def OnLeave(self):
        # on some platforms (Windows) OnLeave is called before every OnDragOver
        # we are delaying cancel to prevent items flickering
        self.delayedCancel.emit()


class DropInternal(wx.FileDropTarget):
    def __init__(self, parent, row, col):
        super().__init__()
        self.parent = parent
        self.col = col
        self.row = row

    def doDragDrop(self, paths):
        data = wx.FileDataObject()
        for path in paths:
            data.AddFile(path)
        dragSource = wx.DropSource(self.parent)
        dragSource.SetData(data)
        dragSource.DoDragDrop()
        self.parent.updateOutputs()

    def move(self, row, col):
        if self.col != col or self.row != row:
            with updateLocker(self.parent):
                items = self.getItemsToMove(col)
                self.parent.trim()
                row = min(row, self.parent.GetItemCount())
                self.parent.insertItems(row, col, items, select=True)
            return True
        else:
            return False

    def getItemsToMove(self, dstCol):
        res = []
        for row in range(self.parent.GetItemCount()):
            for col in range(2):
                cell = self.parent.GetItemWindow(row, col)
                if cell.selected and cell.item is not None:
                    if col != dstCol:
                        if not selectStreamForCol(cell.item, dstCol):
                            cell.select(False)
                            continue
                    res.append(cell.item)
                    cell.setState(None)
        return res

    def OnDropFiles(self, x, y, paths):
        return True

    def OnDragOver(self, x, y, result):
        col = self.parent.getInputCol(x)
        if col is not None:
            row = self.parent.getRow(x, y)
            if self.move(row, col):
                self.col = col
                self.row = self.parent.getRow(x, y)
        return result


def selectStreamForCol(item, col):
    types = RefFile.types
    if col == 0:
        types = SubFile.types

    if item.hasMatchingStream(types):
        item.selectFirstMatchingStream(types)
        return True
    else:
        return False
