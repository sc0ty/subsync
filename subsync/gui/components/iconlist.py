import wx


class IconList(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.InsertColumn(0, _('name'))
        self.data = []

    def InsertItem(self, text, icon=None, item=None):
        no = self.GetItemCount()
        if icon != None:
            super().InsertItem(no, text, self.images[icon])
        else:
            super().InsertItem(no, text)
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.data.append(item)

    def SelectItem(self, data):
        try:
            no = self.data.index(data)
            self.Select(no)
        except:
            self.Select(wx.NOT_FOUND)

    def GetSelectedItem(self):
        no = self.GetFirstSelected()
        if no != wx.NOT_FOUND:
            return self.data[no]

    def SetIconMap(self, imgs):
        img = next(iter(imgs.values()))
        self.imageList = wx.ImageList(img.GetWidth(), img.GetHeight())
        self.images = { status: self.imageList.Add(img) for status, img in imgs.items() }
        self.images[None] = wx.NOT_FOUND
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)

    def SetIcon(self, icon, no=None, item=None):
        if item != None:
            no = self.data.index(item)
        image = self.images[icon]
        x = self.GetItem(no)
        if image != x.GetImage():
            x.SetImage(image)
            self.SetItem(x)
