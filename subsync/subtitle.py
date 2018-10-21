from error import Error
import bisect
import pysubs2
import copy
import re
import threading

import logging
logger = logging.getLogger(__name__)


formatRe  = re.compile(r'{\\.*?}')
newlineRe = re.compile(r'\\[nN]')


class Subtitles(pysubs2.SSAFile):
    def __init__(self):
        super().__init__()
        self.out = None

    def add(self, begin, end, text):
        entry = parseLine(text)
        event = pysubs2.SSAEvent(
                type = 'Dialogue',
                start = begin * 1000.0,
                end = end * 1000.0,
                **entry)
        self.insert(bisect.bisect_left(self, event), event)

    def synchronize(self, formula):
        res = copy.deepcopy(self)
        res.transform_framerate(formula.a*25.0, 25.0)
        res.shift(s=formula.b)
        return res

    def save(self, path, encoding=u'utf-8', fmt=None, fps=None):
        if fmt == None and path.endswith('.txt'):
            fmt = 'microdvd'

        try:
            super().save(path, encoding=encoding, format_=fmt, fps=fps)
        except pysubs2.exceptions.UnknownFileExtensionError as err:
            if fmt != None:
                return Error('Can\'t save subtitles file' + '\n' + str(err)) \
                        .add('path', path) \
                        .add('encodings', encoding) \
                        .addn('format', fmt) \
                        .addn('fps', fps)
            else:
                super().save(path, encoding=encoding, format_='microdvd', fps=fps)

    def getMaxChange(self, formula):
        if len(self.events) > 0:
            return max(abs(formula.getY(x) - x) for x in
                    (self.events[0].start/1000.0, self.events[-1].end/1000.0))
        else:
            return 0.0


class SubtitlesCollector(object):
    def __init__(self):
        self.subtitles = Subtitles()
        self.subtitlesLock = threading.Lock()

    def __len__(self):
        with self.subtitlesLock:
            return len(self.subtitles)

    def addSubtitle(self, begin, end, text):
        with self.subtitlesLock:
            self.subtitles.add(begin, end, text)

    def getMaxSubtitleDiff(self, formula):
        with self.subtitlesLock:
            return self.subtitles.getMaxChange(formula)

    def getSubtitles(self):
        return self.subtitles

    def getSynchronizedSubtitles(self, formula):
        logger.info('subtitles synchronized with %s', str(formula))
        with self.subtitlesLock:
            return self.subtitles.synchronize(formula)


def makeTimestamp(time, short=False, fraction=True):
    t = int(time)
    h = int(t / 3600)
    m = int((t % 3600) / 60)
    s = int(t % 60)

    if short:
        if t < 3600:
            res = '{:d}:{:02d}'.format(m, s);
        else:
            res = '{:d}:{:02d}:{:02d}'.format(h, m, s);
    else:
        res = '{:02d}:{:02d}:{:02d}'.format(h, m, s);

    if fraction:
        ms = int((time % 1) * 1000)
        res += '.{:03d}'.format(ms)
    return res


def parseLine(text):
    fields = text.split(',', 8)
    if len(fields) == 9:
        entry = {
            'style':   fields[2],
            'name':    fields[3],
            'marginl': fields[4],
            'marginr': fields[5],
            'marginv': fields[6],
            'effect':  fields[7],
            'text':    fields[8] }
    else:
        entry = {
            'style': 'Default',
            'text':  text }
    return entry

def extractText(text, linesep='\n'):
    global newLineRe
    global formatRe
    return newlineRe.sub(linesep, formatRe.sub('', parseLine(text)['text']))

