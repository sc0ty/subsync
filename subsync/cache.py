from subsync.settings import settings


class WordsCache(object):
    def __init__(self):
        self.init(None)

    def mkId(self, stream):
        if stream:
            return (stream.path, stream.no, settings().minWordProb, settings().minWordLen)

    def init(self, id):
        self.id = self.mkId(id)
        self.data = []
        self.progress = []

    def isValid(self, id):
        return self.mkId(id) == self.id

    def isEmpty(self):
        return not (self.id or self.data or self.progress)

    def clear(self):
        self.id = None
        self.data = []
        self.progress = None
