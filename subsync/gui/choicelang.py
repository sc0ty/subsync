import wx


class ChoiceLang(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initLangs()

    def initLangs(self):
        from subsync.data.languages import languages

        self.Append(_('<other>'), None)
        self.addSortedLangs({ languages[c][0]: c for c in languages.keys() })

    def addSortedLangs(self, langs):
        for name in sorted(langs):
            self.Append(name, langs[name])

    def SetValue(self, lang):
        if lang != None:
            lang = lang.lower()
            for i in range(1, self.GetCount()):
                if self.GetClientData(i) == lang:
                    self.SetSelection(i)
                    return True
        self.SetSelection(0)
        return False

    def GetValue(self):
        i = self.GetSelection()
        return self.GetClientData(i) if i != -1 else None


class ChoiceGuiLang(ChoiceLang):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initLangs(self):
        from subsync.data.languages import languages, languages2to3
        from subsync.translations import listLanguages as langs

        self.Append(_('default'), None)
        self.addSortedLangs({
            languages.get(languages2to3.get(x), [x])[0]: x for x in langs()})
