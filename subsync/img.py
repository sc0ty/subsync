import wx
import os
from subsync import config
import logging
logger = logging.getLogger(__name__)


def getBitmapPath(name):
    path = os.path.join(config.imgdir, name + '.png')
    if os.path.isfile(path):
        return path

    logger.warning('cannot load image %s from %s', name, path)


def getBitmap(name):
    path = getBitmapPath(name)
    return wx.Bitmap(path)


def setWinIcon(win, id='icon', client=wx.ART_OTHER):
    try:
        icon = wx.Icon(wx.ArtProvider.GetBitmap(id, client))
        win.SetIcon(icon)
    except Exception as e:
        logger.warning('cannot set icon, %r', e)


class ArtProvider(wx.ArtProvider):
    def __init__(self):
        super().__init__()
        self.ids = {}

        self.register('logo', 'logo', wx.ART_OTHER)
        self.register('icon', 'icon', wx.ART_OTHER)

        self.register('tickmark', wx.ART_TICK_MARK)
        self.register('crossmark', wx.ART_CROSS_MARK)
        self.register('info', wx.ART_TIP)
        self.register('error', wx.ART_ERROR)
        self.register('run', 'run')
        self.register('wait', 'wait')
        self.register('dir', wx.ART_FOLDER)

        self.register('file-add', wx.ART_NORMAL_FILE)
        self.register('file-remove', wx.ART_DELETE)
        self.register('props', wx.ART_HELP_SETTINGS)

        self.register('ok', 'selected-file', wx.ART_FRAME_ICON)
        self.register('audio-file', 'audio-file', wx.ART_FRAME_ICON)
        self.register('subtitle-file', 'subtitle-file', wx.ART_FRAME_ICON)
        self.register('video-file', 'video-file', wx.ART_FRAME_ICON)
        self.register('unknown-file', 'unknown-file', wx.ART_FRAME_ICON)

    def register(self, name, id, *clients):
        if type(id) is bytes:
            id = id.decode('utf8')

        if not clients:
            clients = [ wx.ART_TOOLBAR, wx.ART_MENU, wx.ART_BUTTON ]

        for client in clients:
            if type(client) is bytes:
                client = client.decode('utf8')
            self.ids[ (id, str(client)) ] = name

    def CreateBitmap(self, id, client, size):
        if type(id) is bytes:
            id = id.decode('utf8')
        if type(client) is bytes:
            client = client.decode('utf8')

        try:
            name = self.ids.get((id, client))
            if name is not None:
                bitmap = getBitmap(name)
                if bitmap is not None:
                    return bitmap

        except Exception as ex:
            logger.warning('canno\'t load bitmap file %s for %s: %r', id, client, ex)

        if not id.startswith('wx'):
            logger.warning('missing bitmap %s for %s (name: %s)', id, client, name)

        return super().CreateBitmap(id, client, size)


wx.ArtProvider.Push(ArtProvider())
