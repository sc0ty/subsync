from .cell import BaseCell
from subsync.gui import errorwin
from subsync.gui.outpatternwin import OutputPatternWin
from subsync.synchro import OutputFile
from subsync.settings import settings
from subsync import error
import wx
import os


class OutputEditCell(BaseCell):
    def __init__(self, parent, item=None, sub=None, ref=None, path=None, selected=False):
        super().__init__(parent)
        self.item = item or OutputFile(path)

        self.setStatusIcon(wx.ART_FOLDER)
        self.setState(sub, ref, path, selected=selected)
        self.setInteractive()

    def setState(self, sub, ref, path=None, selected=False):
        if path is not None:
            self.item.path = path

        if sub is not None and ref is not None:
            path = self.item.getPath(sub, ref)
            self.m_textName.SetLabel(os.path.basename(path))
            self.m_textDetails.SetLabel(os.path.dirname(path))

        self.select(selected, force=not self.visible)
        self.show(sub is not None and ref is not None)
        self.Layout()
        self.parent.updateEvent.emit()

    def select(self, selected=True, force=False):
        if super().select(selected) or force:
            if self.selected:
                self.setIcon('selected-file')
            else:
                self.setIcon('subtitle-file')

    def show(self, show=True):
        self.m_bitmapStatus.Show(show)
        super().show(show)

    def isFile(self):
        return True

    def showPropsWin(self):
        self.parent.clearSelection(exclude=[ self ])
        self.parent.setPickedCell(self)
        self.select()

        with OutputPatternWin(self, self.item.path) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pattern = dlg.getPattern()
                self.item.path = pattern
                self.parent.outPattern = pattern
                self.parent.updateOutputs()
                settings().set(batchOutPattern=pattern)

    def onLeftDClick(self, event):
        if self.visible:
            self.showPropsWin()
        event.Skip()


class OutputSyncCell(BaseCell):
    def __init__(self, parent, item, sub, ref):
        super().__init__(parent)
        self.item = item
        self.status = None
        self.success = None
        self.errors = error.ErrorsCollector()

        self.setIcon('subtitle-file')
        self.m_textName.SetLabel(os.path.basename(item.getPath(sub, ref)))
        self.setDescription(_('queued...'))
        self.setStatusIcon('wait')
        self.m_bitmapStatus.Show()

        self.show()
        self.select(False)

        self.m_textErrors.Bind(wx.EVT_LEFT_UP, self.onErrorsClick)

    def setDescription(self, description, icon=None, status=None):
        if status is not None:
            description += _(', {} points').format(status.points)
        self.m_textDetails.SetLabel(description)

    def jobStart(self):
        self.setDescription('initializing...')
        self.setStatusIcon('run')

    def update(self, status):
        if self.status is None or status.points != self.status.points:
            self.setDescription(_('synchronizing'), status=status)
            self.status = status

    def jobEnd(self, status, success, terminated, path=None):
        self.status = status or self.status
        self.success = success

        if path:
            self.m_textName.SetLabel(os.path.basename(path))

        if success:
            self.setDescription(_('done'), status=self.status)
            self.setStatusIcon(wx.ART_TICK_MARK)

        else:
            if self.errors:
                self.setStatusIcon(wx.ART_ERROR)
            elif terminated:
                self.setStatusIcon('wait')
            else:
                self.setStatusIcon(wx.ART_CROSS_MARK)

            if terminated:
                self.setDescription(_('terminated'), status=self.status)
            else:
                self.setDescription(_('couldn\'t synchronize'), status=self.status)

    def addError(self, source, error):
        if not self.errors:
            self.m_textErrors.Show()
            self.Layout()
        msg = errorwin.syncErrorToString(source, error)
        self.errors.add(msg, source, error)

    def onErrorsClick(self, event):
        if self.errors:
            errorwin.showErrorDetailsDlg(self, self.errors.getDetails(), _('Error'))
