import gizmo
from subsync.synchro.channels import ChannelsMap
from subsync.data import languages
from subsync import utils
from subsync.error import Error
import os


class InputFile(object):
    def __init__(self, path=None, types=None, stream=None):
        self.path    = path
        self.no      = None
        self.type    = None
        self.types   = types
        self.streams = {}
        self.fps     = None
        self.lang    = None
        self.enc     = None
        self.channels = ChannelsMap.auto()
        self.filetype = None

        if path != None:
            self.open(path)

        if stream != None:
            self.assign(stream)

    def __lt__(self, other):
        if self.path != other.path:
            return self.path < other.path
        return self.no < other.no

    def stream(self):
        return self.streams[self.no] if self.no != None else None

    def open(self, path):
        ss = gizmo.Demux(path).getStreamsInfo()
        streams = {s.no: s for s in ss}

        for t in [ 'video', 'audio', 'subtitle/text' ]:
            if t in [ s.type for s in ss ]:
                self.filetype = t
                break

        self.path = path
        self.streams = streams
        self.no = None
        self.lang = None
        self.enc = None
        self.channels = ChannelsMap.auto()
        self.fps = None

        for stream in ss:
            if stream.frameRate:
                self.fps = stream.frameRate
                break

        if len(streams) > 0:
            self.selectFirstMatchingStream()

    def assign(self, s):
        self.path    = s.path
        self.no      = s.no
        self.type    = s.type
        self.types   = s.types
        self.streams = s.streams
        self.fps     = s.fps
        self.lang    = s.lang
        self.enc     = s.enc
        self.channels= s.channels
        self.filetype= s.filetype

    def setNotNone(self, **kw):
        for key, val in kw.items():
            if val != None:
                setattr(self, key, val)

    def select(self, no):
        stream = self.streams[no]
        self.no = no
        self.type = stream.type
        self.lang = stream.lang

        if not self.lang or self.lang.lower() == 'und':
            self.lang = getLangFromPath(self.path)

        return stream

    def selectBy(self, type=None, lang=None):
        for s in self.streams.values():
            if self.types and s.type not in self.types:
                continue
            if type and not s.type.startswith(type):
                continue
            if lang and lang != s.lang.lower():
                continue
            return self.select(s.no)
        err = Error(_('There is no matching stream in ') + self.path).add('path', self.path)
        if type: err.add('type', type)
        if lang: err.add('language', lang)
        raise err

    def selectFirstMatchingStream(self, types=None):
        if types is not None:
            self.types = types
        if self.streams == None or len(self.streams) == 0:
            return None
        if self.types == None:
            return self.select(min(self.streams))
        for t in self.types:
            for no in sorted(self.streams):
                if self.streams[no].type == t:
                    return self.select(no)

    def hasMatchingStream(self, types=None):
        types = types or self.types
        if types is None:
            return len(self.streams) > 0
        for s in self.streams.values():
            if s.type in types:
                return True
        return False

    def isOpen(self):
        return self.path != None

    def isSelect(self):
        return self.path != None and self.no != None

    def getBaseName(self):
        return self.path and os.path.basename(self.path)

    def serialize(self):
        res = {}
        if self.path: res['path'] = self.path
        if self.no is not None: res['stream'] = self.no + 1
        if self.lang: res['lang'] = self.lang
        if self.enc: res['enc'] = self.enc
        if self.fps: res['fps'] = self.fps
        if self.channels and self.channels.type != 'auto':
            res['channels'] = self.channels.serialize()
        return res

    def deserialize(data, types=None):
        if data:
            path = data.get('path')
            res = InputFile(path=path, types=types)
            if 'stream' in data:
                res.select(data['stream'] - 1)
            elif 'streamByType' in data or 'streamByLang' in data:
                res.selectBy(type=data['streamByType'], lang=data['streamByLang'])
            res.setNotNone(lang=data.get('lang'), enc=data.get('enc'), fps=data.get('fps'))
            if 'channels' in data:
                res.channels = ChannelsMap.deserialize(data['channels'])
            return res

    def __repr__(self):
        return utils.fmtobj(self.__class__.__name__,
                path = '{}:{}/{}'.format(self.path, self.no, len(self.streams)),
                type = self.type,
                lang = self.lang,
                enc = self.enc,
                fps = self.fps,
                channels = self.channels if self.channels.type != 'auto' else None)

    def __str__(self):
        return utils.fmtstr(
                '{}:{}/{}'.format(self.path, self.no, len(self.streams)),
                type = self.type,
                lang = self.lang,
                enc = self.enc,
                fps = self.fps,
                channels = self.channels if self.channels.type != 'auto' else None)


class SubFile(InputFile):
    types = ('subtitle/text',)

    def __init__(self, *args, **kw):
        super().__init__(types=SubFile.types, *args, **kw)

    def deserialize(data):
        return InputFile.deserialize(data, types=SubFile.types)


class RefFile(InputFile):
    types = ('subtitle/text', 'audio')

    def __init__(self, *args, **kw):
        super().__init__(types=RefFile.types, *args, **kw)

    def deserialize(data):
        return InputFile.deserialize(data, types=RefFile.types)


def getLangFromPath(path):
    ''' Returns two- or three-letters language code from filename in form
    name.code.extension, e.g. subtitles.eng.srt or subtitles-fr.srt
    '''

    name = path.rsplit('.', 1)[0]
    size = 0

    for c in reversed(name):
        if c.isalpha():
            size += 1
        else:
            break

    if size == 2 or size == 3:
        return languages.get(name[-size:].lower()).code3
