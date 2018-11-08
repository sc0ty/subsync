import gizmo


class Stream(object):
    def __init__(self, path=None, types=None, stream=None):
        self.path    = path
        self.no      = None
        self.type    = None
        self.types   = types
        self.streams = {}
        self.fps     = None
        self.lang    = None
        self.enc     = None
        self.channels= None

        if path != None:
            self.open(path)

        if stream != None:
            self.assign(stream)

    def stream(self):
        return self.streams[self.no] if self.no != None else None

    def open(self, path):
        ss = gizmo.Demux(path).getStreamsInfo()
        streams = {s.no: s for s in ss if self.types==None or s.type in self.types}

        self.path = path
        self.streams = streams
        self.no = None
        self.lang = None
        self.enc = None
        self.channels = None
        self.fps = None

        for stream in ss:
            if stream.frameRate:
                self.fps = stream.frameRate
                break

        if len(streams) > 0:
            self.selectFirstMachingStream()

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

    def setNotNone(self, **kw):
        for key, val in kw.items():
            if val != None:
                setattr(self, key, val)

    def select(self, no):
        stream = self.streams[no]
        self.no = no
        self.type = stream.type
        self.lang = stream.lang
        return stream

    def selectFirstMachingStream(self):
        if self.streams == None or len(self.streams) == 0:
            return None
        if self.types == None:
            return self.select(min(self.streams))
        for t in self.types:
            for no in sorted(self.streams):
                if self.streams[no].type == t:
                    return self.select(no)

    def isOpen(self):
        return self.path != None

    def isSelect(self):
        return self.path != None and self.no != None

    def __repr__(self):
        return '{}:{}/{} type={} lang={} enc={}'.format(
                self.path, self.no, len(self.streams), self.type, self.lang, self.enc)
