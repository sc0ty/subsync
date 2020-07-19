import gizmo
from subsync.translations import _


class ChannelsMap(object):
    def auto():
        return AutoChannelsMap()

    def all():
        return AllChannelsMap()

    def custom(cm):
        return CustomChannelsMap(cm)

    def deserialize(cm):
        if cm == 'auto' or cm == None:
            return AutoChannelsMap()
        elif cm == 'all':
            return AllChannelsMap()
        else:
            return CustomChannelsMap(cm)

    def getChannelDescription(ch):
        name = gizmo.AudioFormat.getChannelName(ch)
        desc = gizmo.AudioFormat.getChannelDescription(ch)
        if name and desc:
            return '{} ({})'.format(desc, name)
        else:
            return 'channel {}'.format(ch)

    def getChannelId(ch):
        try:
            return gizmo.AudioFormat.getChannelIdByName(ch) or int(ch)
        except:
            return None

    def getChannelName(ch):
        return gizmo.AudioFormat.getChannelName(ch) or str(ch)

    def layoutToIds(layout):
        i = 1
        res = []
        while i <= layout:
            if i & layout:
                res.append(i)
            i <<= 1
        return res

    def __repr__(self):
        return self.serialize()


class AutoChannelsMap(ChannelsMap):
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

    def serialize(self):
        return 'auto'


class AllChannelsMap(ChannelsMap):
    type = 'all'

    def getLayoutMap(self, layout):
        return CustomChannelsMap(layout)

    def getDescription(self):
        return _('all channels')

    def serialize(self):
        return 'all'


class CustomChannelsMap(ChannelsMap):
    type = 'custom'

    def __init__(self, channels):
        if isinstance(channels, str):
            names = channels.replace(' ', '').split(',')
            chs = [ ChannelsMap.getChannelId(name.upper()) for name in names ]
            self.channels = [ ch for ch in chs if ch ]
        elif isinstance(channels, int):
            self.channels = ChannelsMap.layoutToIds(channels)
        else:
            self.channels = channels

    def getLayoutMap(self, layout):
        cl = ChannelsMap.layoutToIds(layout)
        intersection = set(self.channels).intersection(set(cl))
        return CustomChannelsMap(intersection)

    def getMap(self):
        gain = 1.0 / len(self.channels)
        return { (i, 1): gain for i in self.channels }

    def getDescription(self, separator=', '):
        names = [ ChannelsMap.getChannelName(ch) for ch in sorted(self.channels) ]
        return separator.join(names)

    def serialize(self):
        return self.getDescription(separator=',')
