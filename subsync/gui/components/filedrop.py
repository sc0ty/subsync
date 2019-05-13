import wx


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, **kwargs):
        wx.FileDropTarget.__init__(self)

        for key, val in kwargs.items():
            setattr(self, key, val)

    def OnDropFiles(self, x, y, filenames):
        if hasattr(self, 'OnDropFile') and len(filenames) > 0:
            return self.OnDropFile(x, y, filenames[0])
        return False


def setFileDropTarget(target, children=True, **kwargs):
    target.SetDropTarget(FileDropTarget(**kwargs))

    if children:
        for child in target.GetChildren():
            if isinstance(child, wx.Window):
                # separate instance of FileDropTarget since will take ownership
                # of it and will destroy it at close
                child.SetDropTarget(FileDropTarget(**kwargs))

