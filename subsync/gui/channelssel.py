import wx


class AudioChannelsSel(wx.MultiChoiceDialog):
    def __init__(self, parent, msg, caption, audio):
        self.pos2id = {}
        self.id2pos = {}

        names = audio.getChannelNames()
        lst = []
        pos = 0

        for id in sorted(names):
            lst.append(names[id])
            self.pos2id[pos] = id
            self.id2pos[id] = pos
            pos += 1

        super().__init__(parent, msg, caption, lst)

    def selectChannels(self, channels):
        if channels:
            self.SetSelections([ self.id2pos[id] for id in channels ])
        else:
            self.SetSelections([])

    def getSelectedChannels(self):
        return [ self.pos2id[id] for id in self.GetSelections() ]

