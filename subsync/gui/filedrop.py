import wx


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, dropTarget, multiple=False):
        wx.FileDropTarget.__init__(self)
        self.dropTarget = dropTarget
        self.multiple = multiple

    def OnDropFiles(self, x, y, filenames):
        if self.dropTarget != None:
            if self.multiple:
                return self.dropTarget(filenames)
            elif len(filenames) > 0:
                return self.dropTarget(filenames[0])
        return False


def setFileDropTarget(target, callback, childrens=True, multiple=False):
    target.SetDropTarget(FileDropTarget(callback, multiple))

    if childrens:
        for child in target.GetChildren():
            if isinstance(child, wx.Window):
                # separate instance of FileDropTarget since will take ownership
                # of it and will destroy it at close
                child.SetDropTarget(FileDropTarget(callback, multiple))

