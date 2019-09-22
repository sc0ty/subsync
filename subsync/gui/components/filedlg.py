import wx
import os
from subsync.settings import settings


def showOpenFileDlg(parent, multiple=False, **args):
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    if multiple:
        style |= wx.FD_MULTIPLE

    if 'defaultFile' not in args:
        args['defaultDir'] = settings().lastdir

    with wx.FileDialog(parent, _('Select file'), style=style, **args) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_OK:
            if multiple:
                paths = fileDialog.GetPaths()
                if paths:
                    settings().set(lastdir=os.path.dirname(paths[0]))
                return paths
            else:
                path = fileDialog.GetPath()
                settings().set(lastdir=os.path.dirname(path))
                return path


def appendExtensionToPath(dlg):
    wildcard = dlg.GetWildcard().split('|')
    path = dlg.GetPath()
    i = 2 * dlg.GetFilterIndex() + 1

    if i >= 0 and i < len(wildcard):
        exts = wildcard[i].split(';')
        if len(exts) == 0:
            return path

        for ext in exts:
            if ext == '*.*' or ext == '*' or path.lower().endswith(ext[1:]):
                return path
        return path + ext[1:]
    else:
        return path


def showSaveFileDlg(parent, **args):
    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    if 'defaultFile' not in args:
        args['defaultDir'] = settings().lastdir

    with wx.FileDialog(parent, _('Select file'), style=style, **args) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_OK:
            path = appendExtensionToPath(fileDialog)
            settings().set(lastdir=os.path.dirname(path))
            return path

