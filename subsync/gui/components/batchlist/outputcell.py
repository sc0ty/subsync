from .cell import BaseCell
from subsync.gui import errorwin
from subsync.gui.outpatternwin import OutputPatternWin
from subsync.synchro import OutputFile
from subsync import img, error
import wx
import os


class OutputEditCell(BaseCell):
    def __init__(self, parent, item=None, sub=None, ref=None, path=None, selected=False):
        super().__init__(parent)
        self.item = item or OutputFile(path)

        img.setItemBitmap(self.m_bitmapStatus, 'dir')
        self.setState(sub, ref, path, selected=selected)
        self.setInteractive()

    def setState(self, sub, ref, path=None, selected=False):
        if path is not None:
            self.item.path = path

        if sub is not None and ref is not None:
            path = self.item.getPath(sub, ref)
            self.m_textName.SetLabel(os.path.basename(path))
            self.m_textDetails.SetLabel(os.path.dirname(path))
            self.show(True)
        else:
            self.show(False)

        self.select(selected)
        self.parent.updateEvent.emit()

    def select(self, selected=True):
        if super().select(selected):
            if self.selected:
                img.setItemBitmap(self.m_bitmapIcon, 'ok')
            else:
                img.setItemBitmap(self.m_bitmapIcon, 'subtitle-file')

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

        img.setItemBitmap(self.m_bitmapIcon, 'subtitle-file')
        self.m_textName.SetLabel(os.path.basename(item.getPath(sub, ref)))
        self.setDescription(_('queued...'), icon='wait')
        self.m_bitmapStatus.Show()

        self.show()
        self.select(False)

        self.m_textErrors.Bind(wx.EVT_LEFT_UP, self.onErrorsClick)

    def setDescription(self, description, icon=None, status=None):
        if status is not None:
            description += _(', {} points').format(status.points)
        self.m_textDetails.SetLabel(description)

        if icon is not None:
            img.setItemBitmap(self.m_bitmapStatus, icon)

    def jobStart(self):
        self.setDescription('initializing...', icon='run')

    def update(self, status):
        if self.status is None or status.points != self.status.points:
            self.setDescription(_('synchronizing'), status=status)
            self.status = status

    def jobEnd(self, status, success, terminated):
        self.status = status or self.status
        self.success = success

        if success:
            self.setDescription(_('done'), icon='tickmark', status=self.status)

        else:
            icon = None
            if self.errors:
                icon = 'error'
            elif terminated:
                icon = 'wait'
            else:
                icon = 'crossmark'

            if terminated:
                self.setDescription(_('terminated'), icon=icon, status=self.status)
            else:
                self.setDescription(_('couldn\'t synchronize'), icon=icon, status=self.status)

    def addError(self, source, error):
        if not self.errors:
            self.m_textErrors.Show()
        msg = errorwin.syncErrorToString(source, error)
        self.errors.add(msg, source, error)

    def onErrorsClick(self, event):
        if self.errors:
            errorwin.showErrorDetailsDlg(self, self.errors.getDetails(), _('Error'))
