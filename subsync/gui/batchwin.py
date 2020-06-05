import subsync.gui.layout.batchwin
from subsync.gui.aboutwin import AboutWin
from subsync.gui.busydlg import BusyDlg
from subsync.gui.suspendlock import SuspendBlocker
from subsync.gui.components import assetsdlg, filedlg, filedrop
from subsync.gui.components.thread import gui_thread
from subsync.gui.components.update import update_lock
from subsync.gui.errorwin import error_dlg, showExceptionDlg
from subsync.synchro import SyncController, SyncTaskList
from subsync.settings import settings
from subsync import img, utils
from subsync.data.filetypes import subtitleWildcard, videoWildcard
from subsync.data import descriptions
import wx
import time

import logging
logger = logging.getLogger(__name__)


class BatchWin(subsync.gui.layout.batchwin.BatchWin):
    def __init__(self, parent, tasks=None):
        super().__init__(parent)
        img.setWinIcon(self)

        self.m_buttonMaxDistInfo.message = descriptions.maxDistInfo
        self.m_buttonEffortInfo.message = descriptions.effortInfo

        self.m_sliderMaxDist.SetValue(settings().windowSize / 60)
        self.m_sliderEffort.SetValue(settings().minEffort * 100)
        self.onSliderMaxDistScroll(None)
        self.onSliderEffortScroll(None)

        # workaround for truncated texts
        self.m_textMaxDist.SetMinSize(wx.Size(int(self.m_textMaxDist.GetSize().width * 1.1), -1))
        self.m_textEffort.SetMinSize(wx.Size(int(self.m_textEffort.GetSize().width * 1.1), -1))

        self.sync = None
        self.closing = False
        self.startTime = 0.0

        self.m_items.updateEvent.addListener(self.onItemsUpdate)

        self.m_buttonAdd.Bind(wx.EVT_BUTTON, lambda e: self.addFiles())
        self.m_buttonRemove.Bind(wx.EVT_BUTTON, self.m_items.onMenuRemoveClick)
        self.m_buttonStreamSel.Bind(wx.EVT_BUTTON, self.m_items.onMenuStreamSelClick)
        self.m_buttonOutSel.Bind(wx.EVT_BUTTON, self.m_items.onMenuPatternClick)
        self.m_buttonAutoSort.Bind(wx.EVT_BUTTON, self.m_items.onMenuAutoSortClick)
        self.Bind(wx.EVT_MENU, lambda e: self.addFiles(), id=self.m_menuItemAddAuto.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.addFiles(0), id=self.m_menuItemAddSubs.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.addFiles(1), id=self.m_menuItemAddRefs.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), id=self.m_menuItemClose.GetId())
        self.Bind(wx.EVT_MENU, self.m_items.onMenuAutoSortClick, id=self.m_menuItemAutoSort.GetId())
        self.Bind(wx.EVT_MENU, self.m_items.onMenuRemoveClick, id=self.m_menuItemRemove.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.m_items.selectColumns([0, 1, 2]), id=self.m_menuItemSelectAll.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.m_items.selectColumns([0]), id=self.m_menuItemSelectSubs.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.m_items.selectColumns([1]), id=self.m_menuItemSelectRefs.GetId())
        self.Bind(wx.EVT_MENU, lambda e: self.m_items.selectColumns([2]), id=self.m_menuItemSelectOuts.GetId())
        self.Bind(wx.EVT_MENU, self.m_items.onMenuStreamSelClick, id=self.m_menuItemStreamSel.GetId())
        self.Bind(wx.EVT_MENU, self.m_items.onMenuPatternClick, id=self.m_menuItemOutSel.GetId())
        self.Bind(wx.EVT_MENU, self.m_items.onMenuPropsClick, id=self.m_menuItemProps.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuAboutClick, id=self.m_menuItemAbout.GetId())

        filedrop.setFileDropTarget(self.m_panelAutoDrop, OnDropFiles=self.onPanelAutoDropFiles)

        if tasks:
            self.m_items.addTasks(tasks)

        self.Layout()

    def start(self):
        tasks = self.m_items.getTasks()

        if assetsdlg.validateAssets(self, tasks, askForLang=True):
            self.m_gaugeTotalProgress.SetRange(100 * len(tasks))
            self.goToSyncMode()

            self.sync = SyncController(listener=self)
            self.sync.synchronize(tasks)
            self.startTime = time.monotonic()

            self.suspendBlocker = SuspendBlocker()
            if settings().preventSystemSuspend:
                self.suspendBlocker.lock()

    def stop(self):
        self.sync and self.sync.terminate()
        self.m_textStatusVal.SetLabel(_('Terminating...'))

    @update_lock
    def goToEditMode(self):
        self.m_panelProgress.Hide()
        self.m_panelSettings.Show()
        self.m_buttonStop.Show()
        self.m_buttonStop.Hide()
        self.m_buttonClose.Show()
        for no in range(self.m_menubar.GetMenuCount()):
            self.m_menubar.EnableTop(no, True)
        self.m_items.setMode(syncMode=False)
        self.Layout()

    @update_lock
    def goToSyncMode(self):
        self.m_items.setMode(syncMode=True)
        self.m_textStatusVal.SetLabel(_('Initializing...'))
        self.m_bitmapStatus.Hide()
        self.m_gaugeCurrentProgress.SetValue(0)
        self.m_gaugeTotalProgress.SetValue(0)
        self.m_panelSettings.Hide()
        self.m_panelSyncDone.Hide()
        self.m_panelProgress.Show()
        self.m_buttonStart.Disable()
        self.m_buttonStop.Show()
        self.m_buttonClose.Hide()
        for no in range(self.m_menubar.GetMenuCount()):
            self.m_menubar.EnableTop(no, False)
        self.Layout()

    @update_lock
    def goToDoneMode(self, terminated):
        failed = sum([ not x.success for x in self.m_items.iterJobs() ])
        errors = sum([ bool(x.errors) for x in self.m_items.iterJobs() ])
        succeeded = not terminated and not failed

        if terminated:
            self.m_textStatusVal.SetLabel(_('Synchronization terminated'))
        elif failed:
            if failed == self.m_items.GetItemCount():
                self.m_textStatusVal.SetLabel(_('Total failure'))
            elif errors:
                self.m_textStatusVal.SetLabel(_('Got errors, synchronization failed'))
            else:
                self.m_textStatusVal.SetLabel(_('Some tasks couldn\'t be synchronized'))
        else:
            if errors:
                self.m_textStatusVal.SetLabel(_('Everything synchronized, but got errors'))
            else:
                self.m_textStatusVal.SetLabel(_('Everything synchronized successfully'))

        icon = None
        if succeeded:
            icon = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_BUTTON)
        elif errors:
            icon = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_BUTTON)
        else:
            icon = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_BUTTON)

        self.m_bitmapStatus.SetBitmap(icon)
        self.m_bitmapStatus.Show()
        self.m_buttonEditFailed.Enable(failed)
        self.m_panelSyncDone.Show()
        self.m_buttonStop.Hide()
        self.m_buttonClose.Show()
        self.m_items.clearSelection()
        self.Layout()

    @gui_thread
    @update_lock
    def onJobStart(self, task):
        no = task.data['no']
        self.m_items.clearSelection()
        self.m_items.selectRow(no)
        self.m_items.EnsureVisible(no)
        self.m_items.getJob(no).jobStart()
        self.onJobUpdate(task)

    @gui_thread
    def onJobEnd(self, task, status, result):
        no = task.data['no']
        self.m_items.getJob(no).jobEnd(status, result)
        self.m_gaugeCurrentProgress.SetValue(100)

    @gui_thread
    def onJobUpdate(self, task, status=None):
        no = task.data['no']
        if status is not None:
            self.m_items.getJob(no).update(status)

        progress = 0.0
        if status is not None:
            progress = status.progress
            effort = settings().minEffort
            if effort:
                progress = min(max(progress, status.effort / effort, 0), 1)
        self.m_gaugeCurrentProgress.SetValue(100 * progress)
        self.m_gaugeTotalProgress.SetValue(100 * (no + progress))

        if self.sync.running():
            self.updateProgressText(no, progress)

    @gui_thread
    @update_lock
    def onFinish(self, terminated):
        self.m_gaugeTotalProgress.SetValue(self.m_gaugeTotalProgress.GetRange())
        self.goToDoneMode(terminated)
        self.suspendBlocker.unlock()

        if terminated:
            result = SyncJobResult(False, True, None)
            for job in self.m_items.iterJobs():
                if not job.ended:
                    job.jobEnd(None, result)

    @gui_thread
    def onError(self, task, source, error):
        if task:
            no = task.data['no']
            self.m_items.getJob(no).addError(source, error)
        else:
            showExceptionDlg(self, error)

    def updateProgressText(self, no, progress):
        total = self.m_items.GetItemCount()
        elapsed = time.monotonic() - self.startTime

        msg = [ _('Task:'), '{} / {}'.format(no+1, total) ]
        if elapsed > 1:
            msg += [ _('Elapsed:'), utils.timeStampFmt(elapsed) ]
        if elapsed > 60 and progress:
            totalProgress = (no + progress) / total
            eta = elapsed / totalProgress - elapsed
            msg += [ _('ETA:'), utils.timeStampApproxFmt(eta) ]

        self.m_textStatusVal.SetLabel(' '.join(msg))

    def onSliderMaxDistScroll(self, event):
        val = self.m_sliderMaxDist.GetValue()
        self.m_textMaxDist.SetLabel(_('{} min').format(val))
        settings().set(windowSize=val * 60)

    def onSliderEffortScroll(self, event):
        val = self.m_sliderEffort.GetValue() / 100
        self.m_textEffort.SetLabel('{:.2f}'.format(val))
        settings().set(minEffort=val)

    @error_dlg
    def onButtonStartClick(self, event):
        settings().save()
        self.start()

    @error_dlg
    def onButtonStopClick(self, event):
        self.stop()
        self.m_buttonStop.Hide()
        self.m_buttonClose.Show()
        self.Layout()

    def onButtonCloseClick(self, event):
        self.Close()

    @error_dlg
    def addFiles(self, col=None):
        wildcard = '|'.join([
                _('All supported files'), subtitleWildcard + ';' + videoWildcard,
                _('Subtitle files'), subtitleWildcard,
                _('Video files'), videoWildcard,
                _('All files'), '*.*' ])

        paths = filedlg.showOpenFileDlg(self, multiple=True, wildcard=wildcard)
        if paths:
            self.m_items.addFiles(paths, col=col)

    @update_lock
    def onButtonEditFailedClick(self, event):
        rows = [ no for no, job in enumerate(self.m_items.iterJobs()) if job.success ]
        for row in reversed(rows):
            self.m_items.removeRow(row)
        self.goToEditMode()

    def onButtonEditAllClick(self, event):
        self.goToEditMode()

    def onButtonEditNewClick(self, event):
        self.m_items.removeAll()
        self.goToEditMode()

    @error_dlg
    def onChoiceLangChoice(self, event):
        lang = self.m_choiceLang.GetValue()
        self.m_items.updateSelectedInputs(lang=lang)

    @update_lock
    def onItemsUpdate(self):
        subLangs = set([ c.item.lang for c in self.m_items.iterSelected(0) if c.isFile() ])
        refLangs = set([ c.item.lang for c in self.m_items.iterSelected(1) if c.isFile() ])
        selLangs = subLangs | refLangs

        isSubSel = bool(subLangs)
        isRefSel = bool(refLangs)
        isOutSel = bool(self.m_items.getFirstSelected(2))

        self.m_buttonRemove.Enable(isSubSel or isRefSel)
        self.m_buttonStreamSel.Enable(isSubSel ^ isRefSel)
        self.m_buttonOutSel.Enable(isOutSel)
        self.m_buttonAutoSort.Enable(isSubSel or isRefSel)

        self.m_menuItemRemove.Enable(isSubSel or isRefSel)
        self.m_menuItemAutoSort.Enable(isSubSel or isRefSel)
        self.m_menuItemStreamSel.Enable(isSubSel ^ isRefSel)
        self.m_menuItemOutSel.Enable(isOutSel)
        self.m_menuItemProps.Enable(isSubSel or isRefSel or isOutSel)

        if len(selLangs) == 1:
            self.m_choiceLang.SetValue(next(iter(selLangs)))
        else:
            self.m_choiceLang.SetValue(wx.NOT_FOUND)

        self.m_choiceLang.Enable(isSubSel or isRefSel)
        self.m_buttonStart.Enable(self.m_items.isReadyToSynchronize())

    def onClose(self, event):
        if not self.closing:
            self.closing = True
            self.m_items.updateEvent.removeListener(self.onItemsUpdate)
            self.stop()

            if self.sync and self.sync.running():
                with BusyDlg(self, _('Terminating, please wait...')) as dlg:
                    dlg.ShowModalWhile(self.sync.running)

        parent = self.GetParent()
        if parent:
            parent.Show()

        if event:
            event.Skip()

    @error_dlg
    def onMenuNewClick(self, event):
        if self.m_items.GetItemCount() > 0:
            msg = _('Do you want to clear all items?')
            title = _('Remove items')
            flags = wx.YES_NO | wx.ICON_QUESTION
            with wx.MessageDialog(self, msg, title, flags) as dlg:
                if dlg.ShowModal() == wx.ID_YES:
                    self.m_items.removeAll()

    @error_dlg
    def onMenuAddFolderClick(self, event):
        style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        with wx.DirDialog(self, _('Select directory'), style=style) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.m_items.addFiles([ dlg.GetPath() ], skipMissing=True)

    @error_dlg
    def onMenuImportClick(self, event):
        wildcard = '*.yaml|*.yaml|{}|*.*'.format(_('All files'))
        path = filedlg.showOpenFileDlg(self, wildcard=wildcard)
        if path:
            tasks = SyncTaskList.load(path)
            self.m_items.removeAll()
            self.m_items.addTasks(tasks)

    @error_dlg
    def onMenuExportClick(self, event):
        wildcard = '*.yaml|*.yaml|{}|*.*'.format(_('All files'))
        path = filedlg.showSaveFileDlg(self, wildcard=wildcard)
        if path:
            tasks = self.m_items.getTasks()
            SyncTaskList.save(tasks, path)

    @error_dlg
    def onMenuAboutClick(self, event):
        AboutWin(self).ShowModal()

    @error_dlg
    def onPanelAutoDropFiles(self, x, y, filenames):
        self.m_items.addFiles(filenames)
        return True
