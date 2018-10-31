import gui.syncwin_layout
import wx
import synchro
import gui.filedlg
import gui.errorwin
import thread
import data.filetypes
from subtitle import Subtitles, makeTimestamp
from settings import settings
import img
import error
import pysubs2.exceptions
import time
import os
import collections


class SyncWin(gui.syncwin_layout.SyncWin):
    def __init__(self, parent, subs, refs):
        gui.syncwin_layout.SyncWin.__init__(self, parent)

        self.m_buttonDebugMenu.SetLabel(u'\u2630')
        img.setItemBitmap(self.m_bitmapTick, 'tickmark')
        img.setItemBitmap(self.m_bitmapCross, 'crossmark')

        if settings().debugOptions:
            import graph
            graph.init()
            self.m_buttonDebugMenu.Show()

        self.m_buttonStop.SetFocus()
        self.Fit()
        self.Layout()

        self.subs = subs
        self.refs = refs

        self.startTime = time.time()
        self.sync = None

        self.isRunning = False
        self.isCorrelated = False
        self.isSubReady = False

        self.errors = collections.OrderedDict()

        self.updateTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onUpdateTimerTick, self.updateTimer)

        # workaround for GUI freeze
        wx.CallAfter(self.init)

    @gui.errorwin.error_dlg
    def init(self):
        self.sync = synchro.Synchronizer(self, self.subs, self.refs)
        self.sync.start()
        self.stats = self.sync.getStats()

        self.isRunning = True
        self.updateTimer.Start(500)

    def onUpdateTimerTick(self, event):
        if self.isRunning:
            stats = self.sync.getStats()
            elapsed = time.time() - self.startTime
            maxChange = self.sync.getMaxChange()

            self.m_textSync.SetLabel(_('Synchronization: {} points').format(stats.points))
            self.m_textElapsedTime.SetLabel(makeTimestamp(elapsed, short=True, fraction=False))
            self.m_textCorrelation.SetLabel('{:.2f} %'.format(100.0 * stats.factor))
            self.m_textFormula.SetLabel(str(stats.formula))
            self.m_textMaxChange.SetLabel(makeTimestamp(maxChange, short=True))

            if not self.isCorrelated and stats.correlated:
                self.isCorrelated = stats.correlated
                self.m_bitmapCross.Hide()
                self.m_bitmapTick.Show()

                if self.isSubReady:
                    self.m_buttonSave.Enable()

                self.Layout()

            if self.sync.isRunning():
                self.setProgress(self.sync.getProgress())
            else:
                self.stop()
                self.setProgress(1.0)

    @thread.gui_thread
    def onSubReady(self):
        self.isSubReady = True
        if self.isCorrelated:
            self.m_buttonSave.Enable()

    @thread.gui_thread_cnt('pendingErrorsNo')
    def onError(self, source, err):
        msg = errorToString(source, err)
        self.addError(source, err, msg, self.pendingErrorsNo.get() <= 0)

    def addError(self, source, err, msg, update=True):
        if len(self.errors) == 0:
            self.m_panelError.Show()

        if msg not in self.errors:
            self.errors[msg] = error.ErrorsGroup(msg)
        self.errors[msg].add(err)

        if update:
            msgs = [ err.message for err in self.errors.values() ]
            self.m_textErrorMsg.SetLabelText('\n'.join(msgs))

            self.Fit()
            self.Layout()

    def setProgress(self, progress):
        if progress != None:
            pr = int(progress * 100)
            self.m_gaugeProgress.SetValue(pr)
            self.m_textProgress.SetLabel(' {:3} % '.format(pr))
        else:
            self.m_gaugeProgress.Pulse()

    def stop(self):
        self.m_buttonStop.Enable(False)
        self.m_buttonStop.Show(False)
        self.m_buttonClose.Enable(True)
        self.m_buttonClose.Show(True)

        if self.isRunning:
            self.isRunning = False
            self.updateTimer.Stop()
            self.sync.stop()

            if self.isCorrelated and self.isSubReady:
                self.m_buttonSave.Enable()
                self.m_bitmapTick.Show()
                self.m_bitmapCross.Hide()
                if abs(self.sync.getMaxChange()) > 0.3:
                    self.m_textStatus.SetLabel(_('Subtitles synchronized'))
                else:
                    self.m_textStatus.SetLabel(_('No need to synchronize, subtitles are good already'))
            else:
                self.m_bitmapTick.Hide()
                self.m_bitmapCross.Show()
                if self.isSubReady:
                    self.m_textStatus.SetLabel(_('Couldn\'t synchronize'))
                else:
                    self.m_textStatus.SetLabel(_('Subtitles not ready'))

        self.m_buttonClose.SetFocus()
        self.m_buttonSave.SetFocus()
        self.Fit()
        self.Layout()

    def ShowModal(self):
        res = super().ShowModal()
        self.onClose(None)  # since EVT_CLOSE is not emitted for modal frame
        return res

    def onClose(self, event):
        self.stop()

        if self.sync:
            self.sync.stop()

            while self.sync.isRunning():
                wx.Yield()

            self.sync.destroy()

        if event:
            event.Skip()

    def onButtonStopClick(self, event):
        if self.isRunning:
            self.stop()
        else:
            self.Close()

    @gui.errorwin.error_dlg
    def onButtonSaveClick(self, event):
        path = self.saveFileDlg(self.refs.path)
        if path != None:
            fps = self.subs.fps if self.subs.fps != None else self.refs.fps
            try:
                self.sync.getSynchronizedSubtitles().save(path, fps=fps)
            except pysubs2.exceptions.Pysubs2Error as err:
                gui.errorwin.showExceptionDlg(self)

    def onTextShowDetailsClick(self, event):
        self.m_panelDetails.Show()
        self.m_textShowDetails.Hide()
        self.Fit()
        self.Layout()

    def onTextHideDetailsClick(self, event):
        self.m_panelDetails.Hide()
        self.m_textShowDetails.Show()
        self.Fit()
        self.Layout()

    def onTextErrorDetailsClick(self, event):
        msgs = []
        for err in self.errors.values():
            msgs.append(err.message)
            msgs += list(err.descriptions)
            items = sorted(err.fields.items())
            msgs += [ '{}: {}'.format(k, error.formatFieldsVals(v, 10)) for k, v in items ]
            msgs.append('')
        showDetailsWin(self, '\n'.join(msgs), _('Error'))

    def saveFileDlg(self, path=None, suffix=None):
        props = {}
        filters = '|'.join('|'.join(x) for x in data.filetypes.subtitleTypes)
        props['wildcard'] = '{}|{}|*.*'.format(filters, _('All files'))
        props['defaultFile'] = self.genDefaultFileName(path, suffix)
        if path:
            props['defaultDir'] = os.path.dirname(path)
        return gui.filedlg.showSaveFileDlg(self, **props)

    def genDefaultFileName(self, path, suffix=None):
        try:
            res = []
            basename, _ = os.path.splitext(os.path.basename(path))
            res.append(basename)

            if suffix:
                res.append(suffix)

            if settings().appendLangCode and self.subs.lang:
                res.append(self.subs.lang)

            res.append('srt')
            return '.'.join(res)
        except Exception as e:
            logger.warning('%r', e)

    def onButtonDebugMenuClick(self, event):
        self.PopupMenu(self.m_menuDebug)

    def onMenuItemEnableSaveClick(self, event):
        self.m_buttonSave.Enable()

    @gui.errorwin.error_dlg
    def onMenuItemSaveGraphClick(self, event):
        import graph
        wildcard = 'Graphviz DOT|*.dot|PNG|*.png|GIF|*.gif|PostScript|*.ps|All files|*.*'
        path = gui.filedlg.showSaveFileDlg(self, wildcard=wildcard)
        if path != None:
            graph.saveGraph(path, [ p.demux for p in self.sync.pipelines ])

    @gui.errorwin.error_dlg
    def onMenuItemShowGraphClick(self, event):
        import graph
        import config
        path = os.path.join(config.assetdir, 'graph.png')
        graph.saveGraph(path, [ p.demux for p in self.sync.pipelines ])
        wx.LaunchDefaultApplication(path)

    @gui.errorwin.error_dlg
    def onMenuItemDumpSubWordsClick(self, event):
        self.saveWordsDlg(self.subs.path, self.sync.correlator.getSubs())

    @gui.errorwin.error_dlg
    def onMenuItemDumpRefWordsClick(self, event):
        self.saveWordsDlg(self.refs.path, self.sync.correlator.getRefs())

    def saveWordsDlg(self, path, words):
        subs = Subtitles()
        for time, text in words:
            subs.add(time, time, text)

        path = self.saveFileDlg(path, suffix='words')
        if path != None:
            fps = self.subs.fps if self.subs.fps != None else self.refs.fps
            subs.save(path, fps=fps)


def errorToString(source, err):
    if source == 'sub':
        if err.fields['module'].startswith('SubtitleDec.decode'):
            return _('Some subtitles can\'t be decoded (invalid encoding?)')
        elif 'terminated' in err.fields:
            return _('Subtitles read failed')
        else:
            return _('Error during subtitles read')
    elif source == 'ref':
        if err.fields['module'].startswith('SubtitleDec.decode'):
            return _('Some reference subtitles can\'t be decoded (invalid encoding?)')
        elif 'terminated' in err.fields:
            return _('Reference read failed')
        else:
            return _('Error during reference read')
    else:
        return _('Unexpected error occurred')


def showDetailsWin(parent, msg, title):
    dlg = wx.lib.dialogs.ScrolledMessageDialog(parent, msg, title,
            size=(800, 500), style=wx.DEFAULT_FRAME_STYLE)
    font = wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
    dlg.SetFont(font)
    dlg.ShowModal()

