from subsync.subtitle import SubtitlesCollector
from subsync.utils import timeStampFractionFmt
import pysubs2


class WordsFileDump(object):
    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs
        self.subs = SubtitlesCollector()
        self.dirty = False

    def __del__(self):
        self.flush()

    def flush(self):
        if self.dirty:
            self.subs.getSubtitles().save(self.path, **self.kwargs)
            self.dirty = False

    def pushWord(self, word):
        self.subs.addSubtitle(word.time, word.time + word.duration, word.text)
        self.dirty = True


class WordsStdoutDump(object):
    def __init__(self, prefix=None):
        self.prefix = prefix

    def pushWord(self, word):
        print('{:>8}: {} - {}: {}'.format(
            self.prefix,
            timeStampFractionFmt(word.time),
            timeStampFractionFmt(word.time + word.duration),
            word.text))

    def flush(self):
        pass
