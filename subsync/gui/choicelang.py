import wx
from data.languages import languages


class ChoiceLang(wx.Choice):
    def __init__(self, *args, **kwargs):
        wx.Choice.__init__(self, *args, **kwargs)
        self.initLangs()

    def initLangs(self):
        self.Append(_('<other>'), None)
        self.addSortedLangs({ languages[c][0]: c for c in languages.keys() })

    def addSortedLangs(self, langs):
        for name in sorted(langs):
            self.Append(name.title(), langs[name])

    def setLang(self, lang):
        if lang != None:
            lang = lang.lower()
            for i in range(1, self.GetCount()):
                if self.GetClientData(i) == lang:
                    self.SetSelection(i)
                    return True
        self.SetSelection(0)
        return False

    def getLang(self):
        i = self.GetSelection()
        return self.GetClientData(i) if i != -1 else None

