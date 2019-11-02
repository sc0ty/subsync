from .cell import BaseCell
from subsync.gui.openwin import OpenWin
from subsync.synchro import InputFile
import wx


class DropPlaceholderItem(object):
    pass


class InputSyncCell(BaseCell):
    def __init__(self, parent, item, selected=False):
        super().__init__(parent)
        self.item = None
        self.setState(item, selected, force=True)

    def setState(self, item, selected=False, force=False):
        if item is not self.item or force:
            self.item = item

            if type(item) is InputFile:
                s = item.stream()
                desc = [ '{} {}: {}'.format(_('stream'), s.no+1, s.type.split('/')[0]) ]

                if item.lang:
                    lang = item.lang
                else:
                    lang = _('auto')
                    if s.lang:
                        lang = '{} ({})'.format(lang, s.lang)
                desc.append('{}: {}'.format(_('language'), lang))

                if item.enc and s.type == 'subtitle/text':
                    desc.append(item.enc)

                self.m_textName.SetLabel(item.getBaseName())
                self.m_textDetails.SetLabel('; '.join(desc))

            elif type(item) is DropPlaceholderItem:
                self.m_textName.SetLabel(_('drop here'))
                self.m_textDetails.SetLabel('')

            self.drawIcon(item)
            self.show(item is not None)
            self.select(selected)
            self.Layout()
            self.parent.updateEvent.emit()

    def drawIcon(self, item):
        if type(item) is InputFile:
            if self.selected:
                self.setIcon('selected-file')
            else:
                self.setIcon( (item.filetype or 'unknown').split('/')[0] + '-file' )
        elif type(item) is DropPlaceholderItem:
            self.setIcon('new-file')


class InputEditCell(InputSyncCell):
    def __init__(self, parent, item=None, selected=False):
        super().__init__(parent, item, selected)
        self.setInteractive()

        for obj in self.objects():
            obj.Bind(wx.EVT_MOTION, self.onMouseMove)
            obj.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)

    def update(self, lang=False, enc=False, channels=False):
        updated = 0
        if self.isFile():
            if lang is not False:
                updated += self.item.lang != lang
                self.item.lang = lang
            if enc is not False and self.item.type == 'subtitle/text':
                updated += self.item.enc != enc
                self.item.enc = enc
            if channels is not False and self.item.type == 'audio':
                updated += self.item.channels != channels
                self.item.channels = channels

            if updated:
                self.setState(self.item, self.selected, force=True)
        return bool(updated)

    def select(self, selected=True):
        if super().select(selected):
            self.drawIcon(self.item)

    def isFile(self):
        return type(self.item) is InputFile

    def onMouseMove(self, event):
        if self.visible is not None and event.Dragging() and event.LeftIsDown():
            self.parent.dragSelection(self)
            # no skip here since source window could be deleted and it would crash
        else:
            event.Skip()

    def onLeftDClick(self, event):
        if self.item is not None:
            self.showPropsWin()
        event.Skip()

    def showPropsWin(self):
        self.parent.clearSelection(exclude=[ self ])
        self.parent.setPickedCell(self)
        self.select()

        with OpenWin(self, self.item, allowOpen=False) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.setState(dlg.file, selected=True)
                self.parent.updateOutputs()

    def onContextMenu(self, event):
        if self.item is not None and not self.selected:
            self.parent.setPickedCell(self)
            self.parent.clearSelection(exclude=[ self ])
        self.select()
        self.parent.showContextMenu(self)

