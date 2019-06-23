import subsync.gui.layout.outpatternwin
from subsync.gui.errorwin import error_dlg
import wx
import os


def chooseOption(options, defaultValue=None):
    for value, selected in options.items():
        if selected:
            return value
    return defaultValue


class OutputPatternWin(subsync.gui.layout.outpatternwin.OutputPatternWin):
    def __init__(self, parent):
        super().__init__(parent)
        self.customFolder = ''
        self.updatePattern()

    def updatePattern(self):
        if self.m_radioFolderSub.GetValue():
            folder = '{sub_dir}'
        elif self.m_radioFolderRef.GetValue():
            folder = '{ref_dir}'
        else:
            folder = self.customFolder

        name = []
        if self.m_radioFileSub.GetValue():
            name.append('{sub_name}')
        else:
            name.append('{ref_name}')

        if self.m_checkFileAppendLang.GetValue():
            name.append('{ref_lang}')
        if self.m_checkFileAppendStreamNo.GetValue():
            name.append('{ref_no}')

        if self.m_radioTypeAss.GetValue():
            name.append('ass')
        elif self.m_radioTypeSsa.GetValue():
            name.append('ssa')
        else:
            name.append('srt')

        pattern = os.path.join(folder, '.'.join(name))
        self.m_textPattern.SetValue(pattern)

    def getPattern(self):
        return self.m_textPattern.GetValue()

    @error_dlg
    def selectCustomFolder(self):
        title = _('Select output directory')
        style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        with wx.DirDialog(self, title, '', style) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.customFolder = dlg.GetPath()

    def onModeSel(self, event):
        predef = self.m_radioPredef.GetValue()
        self.m_panelPredef.Enable(predef)
        self.m_panelCustom.Enable(not predef)
        if predef:
            self.updatePattern()

    def onNameSel(self, event):
        customFolder = self.m_radioFolderCustom.GetValue()
        self.m_buttonFolderCustom.Enable(customFolder)

        if customFolder and not self.customFolder:
            self.selectCustomFolder()

        self.updatePattern()

    def onButtonFolderCustomClick(self, event):
        self.selectCustomFolder()
        self.updatePattern()

