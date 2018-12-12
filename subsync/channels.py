import gizmo

audio_channel_center_id = 4


def getChannelId(ch):
    try:
        return gizmo.AudioFormat.getChannelIdByName(ch) or int(ch)
    except:
        return None


def getChannelName(ch):
    return gizmo.AudioFormat.getChannelName(ch) or str(ch)


def getChannelDescription(ch):
    name = gizmo.AudioFormat.getChannelName(ch)
    desc = gizmo.AudioFormat.getChannelDescription(ch)
    if name and desc:
        return '{} ({})'.format(desc, name)
    else:
        return 'channel {}'.format(ch)


def layoutToIds(layout):
    i = 1
    res = []
    while i <= layout:
        if i & layout:
            res.append(i)
        i <<= 1
    return res


def getChannelsMap(cm):
    if cm == 'auto' or cm == None:
        return AutoChannelsMap()
    elif cm == 'all':
        return AllChannelsMap()
    else:
        return CustomChannelsMap(cm)


class AutoChannelsMap(object):
    type = 'auto'
    centerId = gizmo.AudioFormat.getChannelIdByName('FC')

    def getLayoutMap(self, layout):
        layoutMap = CustomChannelsMap(layout)
        if self.centerId in layoutMap.channels:
            return CustomChannelsMap(self.centerId)
        else:
            return layoutMap

    def getDescription(self):
        return _('auto')

    def __str__(self):
        return 'auto'


class AllChannelsMap(object):
    type = 'all'

    def getLayoutMap(self, layout):
        return CustomChannelsMap(layout)

    def getDescription(self):
        return _('all channels')

    def __str__(self):
        return 'all'


class CustomChannelsMap(object):
    type = 'custom'

    def __init__(self, channels):
        if isinstance(channels, str):
            names = channels.replace(' ', '').split(',')
            chs = [ getChannelId(name.upper()) for name in names ]
            self.channels = [ ch for ch in chs if ch ]
        elif isinstance(channels, int):
            self.channels = layoutToIds(channels)
        else:
            self.channels = channels

    def getLayoutMap(self, layout):
        cl = layoutToIds(layout)
        intersection = set(self.channels).intersection(set(cl))
        return CustomChannelsMap(intersection)

    def getMap(self):
        gain = 1.0 / len(self.channels)
        return { (i, 1): gain for i in self.channels }

    def getDescription(self, separator=', '):
        names = [ getChannelName(ch) for ch in sorted(self.channels) ]
        return separator.join(names)

    def __str__(self):
        return self.getDescription(separator=',')
