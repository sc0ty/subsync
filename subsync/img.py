import wx
import os
import config
import logging
logger = logging.getLogger(__name__)


_images = {}
_imgdir = ''


def init():
    global _imgdir
    for d in config.imgdirs:
        if os.path.isdir(d):
            _imgdir = d
            break

    if not _imgdir:
        logger.warning('cannot find images directory, tried %s', str(config.imgdirs))

init()


def getBitmapPath(name):
    path = os.path.join(_imgdir, name + '.png')
    if os.path.isfile(path):
        return path

    logger.warning('cannot load image %s', name)
    return None


def getBitmap(name):
    if name not in _images:
        path = getBitmapPath(name)
        if path != None:
            _images[name] = wx.Bitmap(path)
        else:
            _images[name] = None
    return _images[name]


def setItemBitmap(item, name, *args, **kwargs):
    img = getBitmap(name)
    if img != None:
        item.SetBitmap(img, *args, **kwargs)

def setWinIcon(win):
    try:
        path = os.path.join(_imgdir, 'icon.png')
        icon = wx.Icon(wx.Bitmap(path, wx.BITMAP_TYPE_ANY))
        win.SetIcon(icon)
    except Exception as e:
        logger.warning('cannot set icon, %r', e)
