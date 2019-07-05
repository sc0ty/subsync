import subsync.gui.layout.batchwin
from subsync.gui.batchitems import InputCol, OutputCol, InputItem
from subsync.gui.outpatternwin import OutputPatternWin
from subsync.gui.streamselwin import StreamSelectionWin
from subsync.gui.openwin import OpenWin
from subsync.gui.batchsyncwin import BatchSyncWin
from subsync.gui.components import assetsdlg
from subsync.gui.components import filedlg
from subsync.gui.errorwin import error_dlg
from subsync.synchro import SyncTask, SyncTaskList, SubFile, RefFile
from subsync.settings import settings
from subsync import img
from subsync.error import Error
from subsync.data.filetypes import subtitleWildcard, videoWildcard
from subsync.data import descriptions
import wx
import os


class BatchWin(subsync.gui.layout.batchwin.BatchWin):
    def __init__(self, parent, tasks=None, mode=None):
        super().__init__(parent)

        self.m_buttonDebugMenu.SetLabel(u'\u22ee') # 2630
        img.setToolBitmap(self.m_toolBarSub, self.m_toolSubAdd, 'file-add')
        img.setToolBitmap(self.m_toolBarSub, self.m_toolSubRemove, 'file-remove')
        img.setToolBitmap(self.m_toolBarSub, self.m_toolSubSelStream, 'props')
        img.setToolBitmap(self.m_toolBarRef, self.m_toolRefAdd, 'file-add')
        img.setToolBitmap(self.m_toolBarRef, self.m_toolRefRemove, 'file-remove')
        img.setToolBitmap(self.m_toolBarRef, self.m_toolRefSelStream, 'props')
        img.setToolBitmap(self.m_toolBarOut, self.m_toolOutPattern, 'props')

        self.m_buttonMaxDistInfo.message = descriptions.maxDistInfo
        self.m_buttonEffortInfo.message = descriptions.effortInfo

        if settings().debugOptions:
            self.m_buttonDebugMenu.Show()

        self.subs = InputCol(self, SubFile.types)
        self.refs = InputCol(self, RefFile.types)
        self.outs = OutputCol()

        self.outPattern = os.path.join('{ref_dir}', '{ref_name}{if:ref_lang:.}{ref_lang}.srt')

        itemHeight = InputCol.getHeight()
        self.m_items.addCol(self.subs, itemHeight)
        self.m_items.addCol(self.refs, itemHeight)
        self.m_items.addCol(self.outs, itemHeight)

        self.tasks = []
        if tasks:
            self.subs.addItems([ InputItem(file=t.sub, types=SubFile.types) for t in tasks ], 0)
            self.refs.addItems([ InputItem(file=t.ref, types=RefFile.types) for t in tasks ], 0)
        self.updateTasks()

        self.mode = mode

        self.m_items.onItemsChange = self.onItemsChange
        self.m_items.onSelection = self.onSelection
        self.m_items.onContextMenu = self.onContextMenu

        self.m_sliderMaxDist.SetValue(settings().windowSize / 60)
        self.m_sliderEffort.SetValue(settings().minEffort * 100)
        self.onSliderMaxDistScroll(None)
        self.onSliderEffortScroll(None)

        self.onItemsChange()
        self.onSelection()
        self.Layout()

    def onItemsChange(self):
        self.updateTasks()
        canStart = len(self.subs) and len(self.subs) == len(self.refs) == len(self.outs)
        self.m_buttonStart.Enable(canStart)
        self.onSelection()

    def onSelection(self):
        subs = self.m_items.getSelectionInCol(self.subs)
        refs = self.m_items.getSelectionInCol(self.refs)
        outs = self.m_items.getSelectionInCol(self.outs)
        files = [ s.file for s in subs + refs ]

        self.m_toolBarSub.EnableTool(self.m_toolSubRemove.GetId(), bool(subs))
        self.m_toolBarSub.EnableTool(self.m_toolSubSelStream.GetId(), bool(subs))

        self.m_toolBarRef.EnableTool(self.m_toolRefRemove.GetId(), bool(refs))
        self.m_toolBarRef.EnableTool(self.m_toolRefSelStream.GetId(), bool(refs))

        self.m_toolBarOut.EnableTool(self.m_toolOutPattern.GetId(), bool(outs))

        langs = set([ s.lang for s in files ])
        self.m_choiceLang.Enable(bool(langs))
        self.m_choiceLang.SetValue(getSingleVal(langs))

        encs = set([ s.enc for s in files if s.type == 'subtitle/text' ])
        self.m_choiceEnc.Enable(bool(encs))
        self.m_choiceEnc.SetValue(getSingleVal(encs))

    def updateTasks(self):
        size = max(len(self.subs), len(self.refs))
        self.outs.resize(size, self.outPattern)
        self.tasks = []

        for i in range(size):
            task = SyncTask(out=self.outs[i].file)
            if i < len(self.subs): task.sub = self.subs[i].file
            if i < len(self.refs): task.ref = self.refs[i].file
            self.outs[i].setPath(task.getOutputPath())
            self.tasks.append(task)

    def onSliderMaxDistScroll(self, event):
        val = self.m_sliderMaxDist.GetValue()
        self.m_textMaxDist.SetLabel(_('{} min').format(val))
        settings().set(windowSize=val * 60)

    def onSliderEffortScroll(self, event):
        val = self.m_sliderEffort.GetValue() / 100
        self.m_textEffort.SetLabel(_('{:.2f}').format(val))
        settings().set(minEffort=val)

    def onButtonOutputSelectClick(self, event):
        event.Skip()

    @error_dlg
    def onButtonStartClick(self, event):
        settings().save()
        self.start()

    def start(self):
        tasks = self.tasks
        if assetsdlg.validateAssets(self, tasks):
            if self.IsModal():
                self.EndModal(wx.ID_OK)
            else:
                self.Close()

            self.updateTasks()
            with BatchSyncWin(self.GetParent(), tasks, mode=self.mode) as dlg:
                dlg.ShowModal()

    @error_dlg
    def onSubAddClick(self, event):
        paths = self.showOpenFileDlg()
        if paths:
            self.m_items.addFiles(self.subs, paths)

    @error_dlg
    def onRefAddClick(self, event):
        paths = self.showOpenFileDlg()
        if paths:
            self.m_items.addFiles(self.refs, paths)

    def showOpenFileDlg(self):
        wildcard = '|'.join([
                _('All supported files'), subtitleWildcard + ';' + videoWildcard,
                _('Subtitle files'), subtitleWildcard,
                _('Video files'), videoWildcard,
                _('All files'), '*.*' ])

        return filedlg.showOpenFileDlg(self, multiple=True, wildcard=wildcard)

    @error_dlg
    def onSubRemoveClick(self, event):
        items = self.m_items.getSelectionInCol(self.subs)
        self.removeItems(items)

    @error_dlg
    def onRefRemoveClick(self, event):
        items = self.m_items.getSelectionInCol(self.refs)
        self.removeItems(items)

    def removeItems(self, items):
        if not items:
            raise Error(_('Select files first'))
        self.m_items.removeItems(items)
        self.m_items.Refresh()

    @error_dlg
    def onSubSelStreamClick(self, event):
        items = self.m_items.getSelectionInCol(self.subs)
        self.showStreamSelectionWindow(items, self.subs.types)

    @error_dlg
    def onRefSelStreamClick(self, event):
        items = self.m_items.getSelectionInCol(self.refs)
        self.showStreamSelectionWindow(items, self.refs.types)

    def showStreamSelectionWindow(self, items, types):
        if not items:
            raise Error(_('Select files first'))
        files = [ item.file for item in items ]
        with StreamSelectionWin(self, files, types) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                for item, selection in zip(items, dlg.getSelection()):
                    if selection != None:
                        item.selectStream(selection)
                self.onSelection()
                self.updateTasks()
                self.m_items.Refresh()

    @error_dlg
    def onOutPatternClick(self, event):
        with OutputPatternWin(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pattern = dlg.getPattern()
                items = self.m_items.getSelectionInCol(self.outs)
                self.outPattern = pattern
                for item in items:
                    item.setPattern(pattern)
                self.updateTasks()
                self.m_items.Refresh()

    @error_dlg
    def onChoiceLangChoice(self, event):
        self.setStreamParams(lang=self.m_choiceLang.GetValue())

    @error_dlg
    def onChoiceEncChoice(self, event):
        self.setStreamParams(enc=self.m_choiceEnc.GetValue())

    def setStreamParams(self, lang=False, enc=False):
        items = self.m_items.getSelectionInCol(self.subs) + self.m_items.getSelectionInCol(self.refs)
        for item in items:
            item.setStreamParams(lang=lang, enc=enc)
        self.updateTasks()
        self.m_items.Refresh()

    def onContextMenu(self, col, item, index):
        if item and col in (self.subs, self.refs):
            self.PopupMenu(self.m_menuItems)

    @error_dlg
    def onMenuItemsRemoveClick(self, event):
        self.removeItems(self.m_items.getSelection())

    @error_dlg
    def onMenuItemsPropsClick(self, event):
        item = next(iter(self.m_items.getSelection()))
        with OpenWin(self, item.file, allowOpen=False) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                item.setFile(dlg.file)
                self.updateTasks()
                self.m_items.Refresh()

    def onButtonDebugMenuClick(self, event):
        self.PopupMenu(self.m_menuDebug)

    @error_dlg
    def onMenuItemDumpListClick(self, event):
        wildcard = '*.yaml|*.yaml|{}|*.*'.format(_('All files'))
        path = filedlg.showSaveFileDlg(self, wildcard=wildcard)
        if path:
            self.updateTasks()
            SyncTaskList.save(self.tasks, path)


def getSingleVal(items, defaultVal=wx.NOT_FOUND):
    if len(items) == 1:
        return next(iter(items))
    else:
        return defaultVal
