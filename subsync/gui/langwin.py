import wx
from subsync.data import languages


class LanguagesWin(wx.SingleChoiceDialog):
    def __init__(self, parent):
        self.langs = [ None ]
        names = [ _('<auto>') ]

        for name, code in sorted([ (lang.name, lang.code3) for lang in languages.languages ]):
            self.langs.append(code)
            names.append(name)

        super().__init__(parent, _('Select language'), _('Languages'), names)

    def SetValue(self, lang):
        try:
            no = self.langs.index(lang)
            self.SetSelection(no)
        except:
            pass

    def GetValue(self):
        sel = self.GetSelection()
        if sel == wx.NOT_FOUND:
            return wx.NOT_FOUND
        else:
            return self.langs[sel]
