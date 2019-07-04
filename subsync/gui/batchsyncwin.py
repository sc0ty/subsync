import subsync.gui.layout.batchsyncwin
from subsync.synchro import Synchronizer, SyncTask
from subsync.gui import busydlg
from subsync.gui import errorwin
from subsync.gui.components.thread import gui_thread
from subsync import utils
from subsync import img
from subsync.settings import settings
from subsync import error
import gizmo
import wx
import os

import logging
logger = logging.getLogger(__name__)


class TaskState(SyncTask):
    def __init__(self, task):
        super().__init__(task.sub, task.ref, task.out)
        self.state = 'idle'
        self.status = None
        self.errors = error.ErrorsCollector()

    def getTask(self):
        return SyncTask(self.sub, self.ref, self.out)

    def __repr__(self):
        return repr(self.getTask())


class BatchSyncWin(subsync.gui.layout.batchsyncwin.BatchSyncWin):
    def __init__(self, parent, tasks, mode=None):
        super().__init__(parent)

        self.currentTask = None
        self.selectedTask = None

        self.tasks = [ TaskState(task) for task in tasks ]
        self.mode = mode

        img.setItemBitmap(self.m_bitmapTick, 'tickmark')
        img.setItemBitmap(self.m_bitmapCross, 'crossmark')
        self.m_gaugeTotalProgress.SetRange(len(self.tasks) * 100)

        self.m_items.SetIconMap({
            'run':         img.getBitmap('run'),
            'idle':        img.getBitmap('idle'),
            'success':     img.getBitmap('tickmark'),
            'fail':        img.getBitmap('crossmark'),
            'run-err':     img.getBitmap('run'),
            'idle-err':    img.getBitmap('idle'),
            'success-err': img.getBitmap('tickmark'),
            'fail-err':    img.getBitmap('error'),
        })

        for task in self.tasks:
            name = os.path.basename(task.getOutputPath())
            self.m_items.InsertItem(name, icon='idle', item=task)

        self.running = True
        self.closing = False
        self.runTime = wx.StopWatch()
        self.sleeper = gizmo.Sleeper()
        self.thread = gizmo.Thread(self.syncJob, name='BatchSync')

    def stop(self):
        self.running = False
        self.sleeper.wake()

    def syncJob(self):
        for no, task in enumerate(self.tasks):
            if self.running:
                self.runTask(task, no)
            else:
                self.updateStatusDone(task, no, status=None, succeeded=False)

        self.updateStatusAllDone()
        self.running = False
        logger.info('thread terminated')

    def runTask(self, task, no):
        logger.info('running task %i: %r', no, task)
        try:
            sync = Synchronizer(task.sub, task.ref)
            sync.onError = self.onError
            self.updateStatusInit(task, no)

            sync.init(runCb=lambda: self.running)
            if self.running:
                sync.start()

            minEffort = settings().minEffort
            effort = -1

            while self.running and sync.isRunning() and effort < minEffort:
                status = sync.getStatus()
                effort = status.effort
                self.updateStatus(task, no, status)
                self.sleeper.sleep(0.5)
        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self.onError('core', err)

        try:
            sync.stop()
            status = sync.getStatus()
            succeeded = self.running and status and status.subReady
            if succeeded:
                try:
                    sync.getSynchronizedSubtitles().save(
                            path=task.getOutputPath(),
                            encoding=task.getOutputEnc(),
                            fps=task.out.fps,
                            overwrite=task.out.overwrite)

                except Exception as err:
                    logger.warning('%r', err, exc_info=True)
                    self.onError('out', err)

            self.updateStatusDone(task, no, status, succeeded)
        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self.onError('core', err)

        sync.destroy()

    @gui_thread
    def updateStatusInit(self, task, no):
        self.currentTask = task
        self.setTaskState(task, 'run')
        self.selectTask(task)

    @gui_thread
    def updateStatus(self, task, no, status):
        task.status = status
        if task is self.selectedTask:
            self.updateSelectedTask()

        progress = status.progress
        effort = settings().minEffort
        if effort:
            progress = min(max(progress, status.effort / effort, 0), 1)

        self.m_gaugeCurrentProgress.SetValue(100 * progress)
        self.m_gaugeTotalProgress.SetValue(100 * (no + progress))
        self.updateTimer((no + progress) / len(self.tasks))

    @gui_thread
    def updateStatusDone(self, task, no, status=None, succeeded=False):
        if succeeded:
            state = 'success'
        else:
            state = 'fail'
        self.setTaskState(task, state)

        if self.running:
            self.m_gaugeCurrentProgress.SetValue(100)
            self.m_gaugeTotalProgress.SetValue(100 * (no + 1))

    @gui_thread
    def updateStatusAllDone(self):
        self.updateTimer()
        self.showCloseButton()

        for task in self.tasks:
            if task.state == 'fail':
                self.m_buttonFixFailed.Show()
                self.m_buttonFixFailed.SetFocus()
                break

        self.Layout()

        if self.mode and self.mode.autoClose:
            self.Close()

    def updateTimer(self, progress=None):
        elapsed = self.runTime.Time() / 1000
        msg = '{}: {}'.format(_('Elapsed'), utils.timeStampFmt(elapsed))

        if elapsed > 60 and progress:
            eta = elapsed / progress - elapsed
            msg += ', {}: {}'.format(_('ETA'), utils.timeStampApproxFmt(eta))
        self.m_textEta.SetLabel(msg)

    def showCloseButton(self):
        if not self.m_buttonClose.IsShown():
            self.m_buttonStop.Hide()
            self.m_buttonClose.Show()
            self.m_buttonClose.SetFocus()
            self.Layout()

    @gui_thread
    def onError(self, source, err):
        if self.currentTask:
            msg = errorwin.syncErrorToString(source, err)
            self.currentTask.errors.add(msg, source, err)

    def selectTask(self, task):
        self.selectedTask = task
        self.m_items.SelectItem(task)
        self.updateSelectedTask()

    def setTaskState(self, task, state):
        if task.state != state:
            task.state = state
            icon = state
            if task.errors:
                icon += '-err'
            self.m_items.SetIcon(item=task, icon=icon)

            if task is self.selectedTask:
                self.updateSelectedTask()

    def updateSelectedTask(self):
        status = self.selectedTask and self.selectedTask.status
        if status:
            self.m_textPoints.SetLabel(str(status.points))
            self.m_textCorrelation.SetLabel('{:.2f} %'.format(100.0 * status.factor))
            self.m_textFormula.SetLabel(str(status.formula))
            self.m_textMaxChange.SetLabel(utils.timeStampFractionFmt(status.maxChange))
        else:
            self.m_textPoints.SetLabel('-')
            self.m_textCorrelation.SetLabel('-')
            self.m_textFormula.SetLabel('-')
            self.m_textMaxChange.SetLabel('-')

        if self.selectedTask:
            msgs = {
                    'run':     _('synchronizing...'),
                    'idle':    _('waiting...'),
                    'success': _('synchronized'),
                    'fail':    _('couldn\'t synchronize')
                    }
            state = self.selectedTask.state
            self.m_textStatus.SetLabel(msgs[state])

            tick = state == 'success'
            if self.m_bitmapTick.IsShown() != tick:
                self.m_bitmapTick.Show(tick)

            cross = state == 'fail'
            if self.m_bitmapCross.IsShown() != cross:
                self.m_bitmapCross.Show(cross)
        else:
            self.m_textStatus.SetLabel('-')

        showErrors = bool(self.selectedTask and self.selectedTask.errors)
        if showErrors != self.m_textErrorTitle.IsShown():
            self.m_textErrorTitle.Show(showErrors)
            self.m_textErrorDetails.Show(showErrors)

        self.Layout()

    def onButtonStopClick(self, event):
        self.stop()
        self.showCloseButton()

    @errorwin.error_dlg
    def onButtonFixFailedClick(self, event):
        if self.IsModal():
            self.EndModal(wx.ID_OK)
        else:
            self.Close()

        tasks = [ task.getTask() for task in self.tasks if task.state != 'success' ]
        if tasks:
            # to avoid circular dependency
            from subsync.gui.batchwin import BatchWin
            with BatchWin(self.GetParent(), tasks) as dlg:
                dlg.ShowModal()

    def onItemsSelected(self, event):
        self.selectedTask = self.m_items.GetSelectedItem()
        self.updateSelectedTask()

    def onTextErrorDetailsClick(self, event):
        if self.selectedTask:
            details = self.selectedTask.errors.getDetails()
            errorwin.showErrorDetailsDlg(self, details, _('Error'))

    def ShowModal(self):
        res = super().ShowModal()
        self.onClose(None)  # since EVT_CLOSE is not emitted for modal frame
        return res

    def onClose(self, event):
        if not self.closing:
            self.closing = True
            self.stop()

            if self.thread.isRunning():
                with busydlg.BusyDlg(self, _('Terminating, please wait...')) as dlg:
                    dlg.ShowModalWhile(self.thread.isRunning)

        if event:
            event.Skip()
