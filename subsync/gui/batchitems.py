import wx
from subsync.gui.components.multicolview import MultiColumnCol
from subsync.gui.components.dc import BitmapMemoryDC
from subsync.synchro import InputFile, OutputFile
from subsync import img
import os


class BaseItem(object):
    def __init__(self):
        self.buffers = [None, None]

    def draw(self, width, height, selected):
        dc = BitmapMemoryDC(width, height, highlighted=selected)

        margin = 4
        x = margin
        y = margin

        icon = self.getIconBitmap()
        if icon:
            dc.DrawBitmap(icon, x, y)
            x += icon.GetWidth() + 2*margin

        dc.setFont(wx.NORMAL_FONT.GetPointSize(), weight=wx.FONTWEIGHT_BOLD)

        maxWidth = width - x - margin
        text = self.getName()
        if text:
            size = dc.drawTextLimited(self.getName(), x, y, maxWidth)
            y += size.Height

        dc.setFont(wx.NORMAL_FONT.GetPointSize(), weight=wx.FONTWEIGHT_NORMAL)

        maxHeight = height - y - margin
        self.drawDescription(dc, x, y, maxWidth, maxHeight)

        return dc.getBitmap()

    def clear(self):
        self.buffers = [None, None]

    def getBitmap(self, width, height, selected):
        bmp = self.buffers[selected]
        if bmp == None or bmp.GetWidth() != width or bmp.GetHeight() != height:
            bmp = self.draw(width, height, selected)
            self.buffers[selected] = bmp
        return bmp

    def getIconBitmap(self):
        return None

    def getName(self):
        return None

    def drawDescription(self, dc, x, y, w, h):
        pass


class InputItem(BaseItem):
    def __init__(self, path=None, file=None, types=None):
        super().__init__()
        if path:
            file = InputFile(types=types, path=path)
        self.file = file

    def __lt__(self, other):
        return self.file.path < other.file.path

    def getIconBitmap(self):
        iconName = (self.file.filetype or 'unknown').split('/')[0] + '-file'
        return img.getBitmap(iconName)

    def getName(self):
        return self.file and self.file.getBaseName()

    def drawDescription(self, dc, x, y, w, h):
        ss = self.file
        s = ss.stream()
        if s:
            desc = [ '{} {}: {}'.format(_('stream'), s.no+1, s.type.split('/')[0]) ]

            if ss.lang:
                lang = ss.lang
            else:
                lang = _('auto')
                if s.lang:
                    lang = '{} ({})'.format(lang, s.lang)
            desc.append('{}: {}'.format(_('language'), lang))

            if ss.enc and s.type == 'subtitle/text':
                desc.append(ss.enc)

            dc.drawTextLimited('; '.join(desc), x, y, w)

    def getPathInfo(self):
        return self.file and '{}:{}'.format(self.file.path, self.file.no+1)

    def hasStreamType(self, types):
        for s in self.file.streams.values():
            if s.type in types:
                return True
        return False

    def setFile(self, file):
        self.file = file
        self.clear()

    def selectStream(self, no):
        if no != self.file.no:
            self.file.select(no)
            self.clear()

    def setStreamParams(self, lang=False, enc=False):
        if lang != False and lang != self.file.lang:
            self.file.lang = lang
        if enc != False and enc != self.file.enc:
            self.file.enc = enc
        if lang != False or enc != False:
            self.clear()

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.file)


class InputCol(MultiColumnCol):
    def __init__(self, types):
        super().__init__()
        self.types = types

    def canAddFiles(self, index):
        return True

    def canAddItems(self, items, index):
        return [ i for i in items if isinstance(i, InputItem) and i.hasStreamType(self.types) ]

    def addItems(self, items, index):
        for item in items:
            file = item.file
            file.types = self.types
            if file.type not in self.types:
                file.selectFirstMatchingStream()
                item.clear()
        return super().addItems(items, index)

    def getItemBitmap(self, index, width, height, selected):
        if index < len(self.items):
            return self.items[index].getBitmap(width, height, selected)

    def getHeight():
        try:
            dc = wx.MemoryDC()
            dc.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            textHeight = dc.GetTextExtent('Test').Height
        except:
            textHeight = 15
        return max(2 * textHeight + 8, 40)


class OutputItem(BaseItem):
    def __init__(self, file=None, path=None):
        super().__init__()
        self.file = file or OutputFile()
        self.path = None

    def setPattern(self, pattern):
        if self.file.path != pattern:
            self.file.path = pattern
            self.setPath(None)

    def setPath(self, path):
        if path != self.path:
            self.path = path
            self.clear()

    def getPathInfo(self):
        return self.path

    def getName(self):
        return self.path and os.path.basename(self.path)

    def drawDescription(self, dc, x, y, w, h):
        text = self.path and os.path.dirname(self.path)
        if text:
            dc.drawTextLimited(text, x, y, w)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.file)


class OutputCol(MultiColumnCol):
    def getItemBitmap(self, index, width, height, selected):
        if index < len(self.items):
            return self.items[index].getBitmap(width, height, selected)

    def canAddFiles(self, index):
        return False

    def canAddItems(self, items, index):
        return [ item for item in items if isinstance(item, OutputItem) ]

    def resize(self, size, pattern=None):
        if len(self.items) > size:
            self.items = self.items[0:size]
        while len(self.items) < size:
            file = OutputFile(pattern)
            self.items.append(OutputItem(file))
