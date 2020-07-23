from .drop import DropExternal, DropInternal
from .inputcell import InputEditCell, InputSyncCell
from .outputcell import OutputEditCell, OutputSyncCell
from subsync.synchro import SyncTask, RefFile, SubFile, ChannelsMap
from subsync.gui import busydlg
from subsync.gui.errorwin import error_dlg, ErrorWin
from subsync.gui.langwin import LanguagesWin
from subsync.gui.charencwin import CharactersEncodingWin
from subsync.gui.channelswin import ChannelsWin
from subsync.gui.streamselwin import StreamSelectionWin
from subsync.gui.outpatternwin import OutputPatternWin
from subsync.gui.components.update import updateLocker, update_lock
from subsync.gui.components.notifier import DelayedSignalNotifier
from subsync.settings import settings
from subsync import error
import wx
from wx.lib.agw import ultimatelistctrl as ulc
from functools import partial
import os

import logging
logger = logging.getLogger(__name__)


class BatchList(ulc.UltimateListCtrl):
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, agwStyle=wx.LC_REPORT | ulc.ULC_HAS_VARIABLE_ROW_HEIGHT \
                        | ulc.ULC_NO_HIGHLIGHT)

        self.updateEvent = DelayedSignalNotifier(0.1)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.rowHeightSet = False

        self.picked = None

        self.InsertColumn(0, _('subtitles'))
        self.InsertColumn(1, _('references'))
        self.InsertColumn(2, _('outputs'))

        self.m_contextMenu = wx.Menu()
        self.m_menuItemLanguage = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('&Language'))
        self.m_contextMenu.Append(self.m_menuItemLanguage)
        self.m_menuItemEncoding = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('Character &encoding'))
        self.m_contextMenu.Append(self.m_menuItemEncoding)
        self.m_menuItemEncoding.Enable(False)
        self.m_menuItemChannels = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('Audio &channels'))
        self.m_contextMenu.Append(self.m_menuItemChannels)
        self.m_menuItemChannels.Enable(False)
        self.m_contextMenu.AppendSeparator()
        self.m_menuItemAutoSort = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('Au&to sort'))
        self.m_contextMenu.Append(self.m_menuItemAutoSort)
        self.m_menuItemRemove = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('&Remove'))
        self.m_menuItemRemove.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU))
        self.m_contextMenu.Append(self.m_menuItemRemove)
        self.m_contextMenu.AppendSeparator()
        self.m_menuItemStreamSel = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('Select &stream'))
        self.m_contextMenu.Append(self.m_menuItemStreamSel)
        self.m_menuItemProps = wx.MenuItem(self.m_contextMenu, wx.ID_ANY, _('&Properties'))
        self.m_contextMenu.Append(self.m_menuItemProps)

        self.SetDropTarget(DropExternal(self))
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_SIZE, self.onResize)

        # workaround for deadlock on Mac
        if wx.Platform == '__WXMAC__':
            freeze = super().Freeze
            thaw = super().Thaw

            def unfreeze(cb):
                def wrapper(*args, **kwargs):
                    level = 0
                    while self.IsFrozen():
                        thaw()
                        level += 1
                    try:
                        cb(*args, **kwargs)
                    finally:
                        for i in range(level):
                            freeze()
                return wrapper

            self.InsertItem = unfreeze(self.InsertItem)
            self.SetItemWindow = unfreeze(self.SetItemWindow)
            self.insertRow = unfreeze(self.insertRow)

        self.Layout()

    def Freeze(self):
        super().Freeze()
        self.updateEvent.disable()

    def Thaw(self):
        self.updateEvent.enable()
        super().Thaw()

    @update_lock
    def setMode(self, syncMode):
        dropTarget = None
        if not syncMode:
            dropTarget = DropExternal(self)
        self.SetDropTarget(dropTarget)
        self.updateEvent.enable(not syncMode)

        for row in range(self.GetItemCount()):
            sub = self.GetItemWindow(row, 0)
            ref = self.GetItemWindow(row, 1)
            out = self.GetItemWindow(row, 2)

            if syncMode:
                nout = OutputSyncCell(self, out.item, sub.item, ref.item)
                nsub = InputSyncCell(self, sub.item)
                nref = InputSyncCell(self, ref.item)
            else:
                nout = OutputEditCell(self, out.item, sub.item, ref.item)
                nsub = InputEditCell(self, sub.item)
                nref = InputEditCell(self, ref.item)

            self.SetItemWindow(row, 0, nsub, expand=True)
            self.SetItemWindow(row, 1, nref, expand=True)
            self.SetItemWindow(row, 2, nout, expand=True)

            sub.Destroy()
            ref.Destroy()
            out.Destroy()

        self.updateEvent.emit()

    @update_lock
    def addTasks(self, tasks):
        for task in tasks:
            row = self.GetItemCount()
            self.insertRow(row, sub=task.sub, ref=task.ref, out=task.out)

    def getTasks(self):
        tasks = []
        for row in range(self.GetItemCount()):
            sub = self.GetItemWindow(row, 0).item
            ref = self.GetItemWindow(row, 1).item
            out = self.GetItemWindow(row, 2).item
            tasks.append( SyncTask(sub, ref, out, data={'no': row}) )
        return tasks

    def getJob(self, no):
        return self.GetItemWindow(no, 2)

    def iterJobs(self):
        for row in range(self.GetItemCount()):
            yield self.GetItemWindow(row, 2)

    def addFiles(self, paths, skipMissing=False, row=None, col=None):
        if isinstance(self.GetDropTarget(), DropInternal):
            # files are dragged from inside so we are removing them to avoid duplication
            self.removeSelected()

        type = RefFile
        if col == 0:
            type = SubFile
        items = self.loadFiles(paths, type, skipMissing=skipMissing)

        subs, refs = [], []
        if col == 0:
            subs = items
        elif col == 1:
            refs = items
        else:
            subs = sorted([ item for item in items if item.filetype == 'subtitle/text' ])
            refs = sorted([ item for item in items if item.filetype != 'subtitle/text' ])

        with updateLocker(self):
            self.clearSelection()

            if row is None:
                row = self.GetItemCount()
                for r in reversed(range(self.GetItemCount())):
                    if subs and self.GetItemWindow(r, 0).item is not None:
                        break
                    if refs and self.GetItemWindow(r, 1).item is not None:
                        break
                    row = r

            if subs:
                self.insertItems(row, 0, subs, select=True)
            if refs:
                self.insertItems(row, 1, refs, select=True)

            self.updateOutputs()
            self.EnsureVisible(row)

    def loadFiles(self, paths, type, skipMissing=False):
        items = []
        errors = []

        def load(paths, skipMissing):
            for path in paths:
                if os.path.isdir(path):
                    for root, _, names in os.walk(path):
                        paths = [ os.path.join(root, name) for name in names ]
                        load(paths, skipMissing=True)
                else:
                    loadFile(path, skipMissing)

        def loadFile(path, skipMissing):
            try:
                item = type(path=path)
                if item.hasMatchingStream():
                    items.append(item)
                elif not skipMissing:
                    errors.append((path, _('There are no usable streams')))

            except Exception as err:
                if not skipMissing or error.getExceptionField(err, 'averror') != 'AVERROR_INVALIDDATA':
                    msg = error.getExceptionMessage(err) + '\n' + error.getExceptionDetails()
                    errors.append((path, msg))

        msg = _('Loading, please wait...')
        busydlg.showBusyDlgAsyncJob(self, msg, load, paths, skipMissing)

        if errors:
            msg = [ _('Following files could not be added:') ]
            msg += [ path for path, _ in errors[:10] ]
            if len(errors) > 10:
                msg.append(_('and {} more').format(len(errors) - 10))

            with ErrorWin(self, '\n'.join(msg)) as dlg:
                for path, msg in errors:
                    dlg.addDetails('FILE ' + path)
                    dlg.addDetails(msg, '\n')
                dlg.ShowModal()

        return items

    def getInputCol(self, x):
        pos = 0
        try:
            # workaround for broken UltimateListCtrl
            pos = -self._mainWin.GetScrollPos(wx.HORIZONTAL)
            thumb = self._mainWin.GetScrollThumb(wx.HORIZONTAL)
            if pos and thumb:
                pos *= self.GetClientSize().width / thumb
            else:
                pos = 0
        except Exception as e:
            logger.warning('getInputCol: gathering scroll position failed: %s', e)

        for col in range(2):
            pos += self.GetColumnWidth(col)
            if x < pos:
                return col

    def getRow(self, x, y):
        try:
            row = self.FindItemAtPos(0, wx.Point(x, y))
            if row != wx.NOT_FOUND:
                return row
        except Exception as e:
            logger.warning('getRow: UltimateListCtrl.FindItemAtPos failed: %s', e)
        return self.GetItemCount()

    def getCellCoords(self, cell):
        for row in range(self.GetItemCount()):
            for col in range(3):
                if self.GetItemWindow(row, col) is cell:
                    return row, col

    @update_lock
    def insertItem(self, row, col, item, select=False):
        if row < self.GetItemCount():
            cell = self.GetItemWindow(row, col)
            if cell.item is None:
                cell.setState(item, select)
                return False

        sub = item if col == 0 else None
        ref = item if col == 1 else None
        self.insertRow(row, sub, ref, select=select)
        return True

    @update_lock
    def insertItems(self, row, col, items, select=False):
        for i, item in enumerate(items):
            self.insertItem(row + i, col, item, select=True)

    @update_lock
    def replaceItem(self, row, col, item, select=False):
        self.GetItemWindow(row, col).setState(item, select)

    # NO @update_lock - workaround for deadlock on Mac - caller should lock itself
    def insertRow(self, row, sub=None, ref=None, out=None, select=False):
        row = min(row, self.GetItemCount())

        item = ulc.UltimateListItem()
        item.SetId(row)
        swin = InputEditCell(self, sub, selected=select)
        item.SetWindow(swin, expand=True)
        self.InsertItem(item)

        rwin = InputEditCell(self, ref, selected=select)
        self.SetItemWindow(row, 1, rwin, expand=True)

        outPath = None
        if out is None:
            outPath = settings().batchOutPattern
        owin = OutputEditCell(self, out, sub, ref, path=outPath, selected=select)
        self.SetItemWindow(row, 2, owin, expand=True)

    @update_lock
    def removeItem(self, row, col):
        if self.GetItemWindow(row, (col+1)%2).item is None:
            self.removeRow(row)
        else:
            self.clearItem(row, col)

    @update_lock
    def clearItem(self, row, col):
        self.GetItemWindow(row, col).setState(None)
        self.GetItemWindow(row, 2).setState(None, None)

    @update_lock
    def removeRow(self, row):
        self.DeleteItem(row)
        self.updateEvent.emit()

    @update_lock
    def removeAll(self):
        # workaround for crashing DeleteAllItems
        for row in reversed(range(self.GetItemCount())):
            self.DeleteItem(row)
        self.updateEvent.emit()

    @update_lock
    def clearSelection(self, *cols, exclude=None):
        for cell in self.iterSelected(*cols):
            if exclude is None or cell not in exclude:
                cell.select(False)
                if self.picked is cell:
                    self.picked = None
        self.updateEvent.emit()

    @update_lock
    def selectRow(self, row):
        for col in range(3):
            self.GetItemWindow(row, col).select()

    @update_lock
    def updateSelectedInputs(self, lang=False, enc=False, channels=False):
        for row in range(self.GetItemCount()):
            sub = self.GetItemWindow(row, 0)
            ref = self.GetItemWindow(row, 1)
            usub = sub.selected and sub.update(lang, enc, channels)
            uref = ref.selected and ref.update(lang, enc, channels)
            if usub or uref:
                out = self.GetItemWindow(row, 2)
                out.setState(sub.item, ref.item)

    @update_lock
    def updateSelectedOutputs(self, path):
        for row in range(self.GetItemCount()):
            out = self.GetItemWindow(row, 2)
            if out.selected and out.item.path is not path:
                sub = self.GetItemWindow(row, 0)
                ref = self.GetItemWindow(row, 1)
                out.setState(sub.item, ref.item, path, selected=True)

    def iterSelected(self, *cols, coords=False):
        cols = cols or range(3)
        for row in range(self.GetItemCount()):
            for col in cols:
                cell = self.GetItemWindow(row, col)
                if cell.selected:
                    if coords:
                        yield row, col, cell
                    else:
                        yield cell

    def isReadyToSynchronize(self):
        for row in range(self.GetItemCount()):
            for col in range(3):
                if not self.GetItemWindow(row, col).isFile():
                    return False
        return self.GetItemCount() > 0

    def getFirstSelected(self, *cols):
        for cell in self.iterSelected(*cols):
            return cell

    @update_lock
    def removeSelected(self):
        for row in reversed(range(self.GetItemCount())):
            sub = self.GetItemWindow(row, 0)
            ref = self.GetItemWindow(row, 1)
            updateOut = sub.selected ^ ref.selected
            if sub.selected:
                self.clearItem(row, 0)
            if ref.selected:
                self.clearItem(row, 1)
            if not sub.visible and not ref.visible:
                self.removeRow(row)
            elif updateOut:
                self.GetItemWindow(row, 2).show(False)

    def setPickedCell(self, cell):
        self.picked = cell

    def getPickedCoords(self):
        if self.picked is not None and self.picked.selected:
            return self.getCellCoords(self.picked)

        self.picked = self.getFirstSelected()
        return self.getCellCoords(self.picked)

    @update_lock
    def selectRange(self, col, row1, row2=None, clearOther=True):
        if row2 is None:
            row2 = row1
            picked = self.getPickedCoords()
            if picked:
                row2 = picked[0]
        if clearOther:
            self.clearSelection()
        for row in range(min(row1, row2), max(row1, row2)+1):
            self.GetItemWindow(row, col).select(True)

    @update_lock
    def selectColumns(self, cols):
        for row in range(self.GetItemCount()):
            for col in range(3):
                cell = self.GetItemWindow(row, col)
                if cell.item is not None:
                    cell.select(col in cols)

    @update_lock
    def trim(self):
        for row in reversed(range(self.GetItemCount())):
            if self.GetItemWindow(row, 0).item is None and self.GetItemWindow(row, 1).item is None:
                self.removeRow(row)

    @update_lock
    def reflow(self, start=0):
        dst = 0
        for src in range(start, self.GetItemCount()):
            sub = self.GetItemWindow(src, 0)
            ref = self.GetItemWindow(src, 1)
            if sub.visible or ref.visible:
                if src != dst:
                    self.GetItemWindow(dst, 0).setState(sub.item)
                    self.GetItemWindow(dst, 1).setState(ref.item)
                    self.GetItemWindow(dst, 2).setState(sub.item, ref.item)
                dst += 1

        for row in range(dst, self.GetItemCount()):
            self.GetItemWindow(row, 0).setState(None)
            self.GetItemWindow(row, 1).setState(None)
            self.GetItemWindow(row, 2).setState(None, None)

        return dst

    @update_lock
    def updateOutputs(self):
        for row in range(self.GetItemCount()):
            sub = self.GetItemWindow(row, 0)
            ref = self.GetItemWindow(row, 1)
            out = self.GetItemWindow(row, 2)
            out.setState(sub and sub.item, ref and ref.item)

    def dragSelection(self, src=None):
        paths = [ cell.item.path for cell in self.iterSelected(0, 1) ]
        if paths:
            coords = self.getCellCoords(src)
            row = coords and coords[0]
            col = coords and coords[1]
            drop = DropInternal(self, row, col)
            self.SetDropTarget(drop)
            self.updateEvent.disable()
            self.clearSelection(2)

            try:
                # will block until drop
                drop.doDragDrop(paths)
            finally:
                self.updateOutputs()
                self.updateEvent.enable()
                self.SetDropTarget(DropExternal(self))
                wx.CallAfter(self.trim)

    @update_lock
    def onLeftDown(self, event):
        self.clearSelection()

    @update_lock
    def onResize(self, event):
        width = self.GetSize().width
        colsw = [ self.GetColumnWidth(col) for col in range(self.GetColumnCount()) ]
        ratio = width / sum(colsw)
        for col, width in enumerate(colsw):
            self.SetColumnWidth(col, int(width * ratio))
        event.Skip()

    def showContextMenu(self, cell=None):
        types = set([ c.item.type for c in self.iterSelected(0, 1) ])
        if types:
            self.m_menuItemEncoding.Enable('subtitle/text' in types)
            self.m_menuItemChannels.Enable('audio' in types)

            menuHandlers = [
                    (self.m_menuItemLanguage.GetId(),  self.onMenuLanguageClick),
                    (self.m_menuItemLanguage.GetId(),  self.onMenuLanguageClick),
                    (self.m_menuItemEncoding.GetId(),  self.onMenuEncodingClick),
                    (self.m_menuItemChannels.GetId(),  self.onMenuChannelsClick),
                    (self.m_menuItemAutoSort.GetId(),  partial(wx.CallAfter, self.onMenuAutoSortClick)),
                    (self.m_menuItemRemove.GetId(),    partial(wx.CallAfter, self.onMenuRemoveClick)),
                    (self.m_menuItemStreamSel.GetId(), self.onMenuStreamSelClick),
                    (self.m_menuItemProps.GetId(),     self.onMenuPropsClick),
                    ]

            try:
                for id, handler in menuHandlers:
                    self.Bind(wx.EVT_MENU, handler=partial(handler, cell=cell), id=id)
                self.PopupMenu(self.m_contextMenu)
            finally:
                for id, _ in menuHandlers:
                    self.Unbind(wx.EVT_MENU, id=id)

    @error_dlg
    def onMenuLanguageClick(self, event, cell=None):
        langs = set([ c.item.lang for c in self.iterSelected(0, 1) ])
        if langs:
            self.clearSelection(2)
            dlg = LanguagesWin(self)
            if len(langs) == 1:
                dlg.SetValue(next(iter(langs)))
            if dlg.ShowModal() == wx.ID_OK and dlg.GetValue() != wx.NOT_FOUND:
                self.updateSelectedInputs(lang=dlg.GetValue())

    @error_dlg
    def onMenuEncodingClick(self, event, cell=None):
        cells = [ c for c in self.iterSelected(0, 1) if c.item.type == 'subtitle/text' ]

        if cells:
            self.clearSelection(exclude=cells)
            dlg = CharactersEncodingWin(self)
            encs = set([ c.item.enc for c in cells ])
            if len(encs) == 1:
                dlg.SetValue(next(iter(encs)))
            if dlg.ShowModal() == wx.ID_OK and dlg.GetValue() != wx.NOT_FOUND:
                self.updateSelectedInputs(enc=dlg.GetValue())

    @error_dlg
    def onMenuPatternClick(self, event, cell=None):
        cell = self.getFirstSelected(2)
        if cell:
            path = cell.item.path
            with OutputPatternWin(self, path) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    self.updateSelectedOutputs(dlg.getPattern())
                    settings().set(batchOutPattern=dlg.getPattern())

    @error_dlg
    def onMenuChannelsClick(self, event, cell=None):
        ids = set()
        for cell in self.iterSelected(0, 1):
            stream = cell.item.stream()
            if cell.item.type == 'audio' and stream is not None and stream.audio is not None:
                ids |= set(ChannelsMap.layoutToIds(stream.audio.channelLayout))

        if ids:
            with ChannelsWin(self, channelIds=ids) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    self.updateSelectedInputs(channels=dlg.GetValue())

    @error_dlg
    @update_lock
    def onMenuAutoSortClick(self, event, cell=None):
        subs = []
        refs = []

        for cell in self.iterSelected(0, 1):
            item = cell.item
            if item.filetype == 'subtitle/text':
                if item.stream() is None or item.stream().type not in SubFile.types:
                    item.selectFirstMatchingStream(SubFile.types)
                subs.append(item)
            else:
                if item.stream() is None or item.stream().type not in RefFile.types:
                    item.selectFirstMatchingStream(RefFile.types)
                refs.append(item)
            cell.setState(None)

        self.trim()
        row = self.GetItemCount()
        self.insertItems(row, 0, sorted(subs), select=True)
        self.insertItems(row, 1, sorted(refs), select=True)
        self.updateOutputs()

    @error_dlg
    def onMenuRemoveClick(self, event, cell=None):
        self.removeSelected()

    @error_dlg
    def onMenuStreamSelClick(self, event, cell=None):
        cell = cell or self.getFirstSelected(0, 1)
        col = [ SubFile.types, RefFile.types ].index(cell.item.types)
        cells = list(self.iterSelected(col))
        self.clearSelection((col + 1) % 2, 2)

        items = [ c.item for c in cells ]
        dlg = StreamSelectionWin(self, items, cell.item.types)
        if dlg.ShowModal() == wx.ID_OK:
            with updateLocker(self):
                for c, selection in zip(cells, dlg.getSelection()):
                    if selection != None:
                        c.item.select(selection)
                        c.setState(c.item, selected=True, force=True)
                self.updateOutputs()

    @error_dlg
    def onMenuPropsClick(self, event, cell=None):
        cell = cell or self.getFirstSelected()
        if cell is not None:
            cell.showPropsWin()
