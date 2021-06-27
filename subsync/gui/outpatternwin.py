import subsync.gui.layout.outpatternwin
from subsync.gui.errorwin import error_dlg
from subsync.synchro import OutputFile
from subsync.gui.components import popups
from subsync.settings import settings
import wx
import re
import os


class OutputPatternWin(subsync.gui.layout.outpatternwin.OutputPatternWin):
    def __init__(self, parent, pattern=None):
        super().__init__(parent)
        self.m_panelCustom.Disable()
        self.customFolder = ''
        if pattern:
            self.setPattern(pattern)

        overwrite = settings().overwriteExistingFiles or settings().overwrite
        self.m_checkOverwriteFiles.SetValue(overwrite)
        self.onModeSel(None)

    def updatePattern(self):
        pattern = self.serializePredefinedPattern()
        self.m_textPattern.SetValue(''.join(pattern))

    def setPattern(self, pattern):
        if pattern and self.deserializePredefinedPattern(pattern):
            self.updatePattern()
        else:
            self.m_radioCustom.SetValue(True)
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
                return True

    def serializePredefinedPattern(self):
        res = []
        if self.m_radioFolderSub.GetValue():
            res.append('{sub_dir}')
        elif self.m_radioFolderRef.GetValue():
            res.append('{ref_dir}')
        else:
            res.append(self.customFolder)

        res.append(os.path.sep)

        if self.m_radioFileSub.GetValue():
            res.append('{sub_name}')
        else:
            res.append('{ref_name}')

        if self.m_checkFileAppendLang.GetValue():
            res.append('{if:sub_lang:.}{sub_lang}')

        if self.m_checkFileAppendLang2.GetValue():
            res.append('{if:sub_lang2:.}{sub_lang2}')

        if self.m_checkFileAppendStreamNo.GetValue():
            res.append('.{ref_no}')

        if self.m_radioTypeAss.GetValue():
            res.append('.ass')
        elif self.m_radioTypeSsa.GetValue():
            res.append('.ssa')
        else:
            res.append('.srt')
        return ''.join(res)

    def deserializePredefinedPattern(self, pattern):
        try:
            p = re.findall(r'{[^}]*}|[^{]+', pattern)
            if p[0].endswith(os.path.sep):
                p = [ p[0][:-1], os.path.sep ] + p[1:]

            if p and len(p) >= 3:
                folder = p[0]
                if folder == '{sub_dir}':
                    self.m_radioFolderSub.SetValue(True)
                elif folder == '{ref_dir}':
                    self.m_radioFolderRef.SetValue(True)
                elif folder and not folder[0] == '{':
                    self.m_radioFolderCustom.SetValue(True)
                    self.m_buttonFolderCustom.Enable(True)
                    self.customFolder = folder
                else:
                    return False

                ext = p[-1]
                if ext == '.srt':
                    self.m_radioTypeSrt.SetValue(True)
                elif ext == '.ass':
                    self.m_radioTypeAss.SetValue(True)
                elif ext == '.ssa':
                    self.m_radioTypeSsa.SetValue(True)
                else:
                    return False

                items = set(p)
                if '{sub_name}' in items:
                    self.m_radioFileSub.SetValue(True)
                elif '{ref_name}' in items:
                    self.m_radioFileRef.SetValue(True)
                else:
                    return False

                self.m_checkFileAppendLang.SetValue('{sub_lang}' in items)
                self.m_checkFileAppendLang2.SetValue('{sub_lang2}' in items)
                self.m_checkFileAppendStreamNo.SetValue('{ref_no}' in items)
                return self.serializePredefinedPattern() == pattern

        except:
            return False

        return False

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
            selected = self.selectCustomFolder()
            if not selected:
                self.m_radioFolderRef.SetValue(True)

        self.updatePattern()

    def onCheckFileAppendLangCheck(self, event):
        self.m_checkFileAppendLang2.SetValue(False)
        self.onNameSel(event)

    def onCheckFileAppendLang2Check(self, event):
        self.m_checkFileAppendLang.SetValue(False)
        self.onNameSel(event)

    def onButtonFolderCustomClick(self, event):
        self.selectCustomFolder()
        self.updatePattern()

    def onCheckOverwriteFiles(self, event):
        overwrite = self.m_checkOverwriteFiles.GetValue()
        if overwrite:
            overwrite = popups.showConfirmationPopup(self,
                    _('Are you sure you want to overwrite output files if they exist?'),
                    _('Overwrite files?'),
                    confirmKey='showOverwriteExistingFilesConfirmPopup')
            self.m_checkOverwriteFiles.SetValue(overwrite)
        settings().set(overwriteExistingFiles=overwrite, overwrite=False)

    @error_dlg
    def onButtonOkClick(self, event):
        OutputFile(self.getPattern()).validateOutputPattern()
        self.EndModal(wx.ID_OK)

