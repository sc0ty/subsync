from subsync import error
from subsync import utils
from subsync.data import filetypes
import bisect
import pysubs2
import copy
import threading
import os

import logging
logger = logging.getLogger(__name__)


class Subtitles(pysubs2.SSAFile):
    def __init__(self):
        super().__init__()

    def setHeader(self, header):
        s = super().from_string(header)
        self.aegisub_project = s.aegisub_project
        self.info = s.info
        self.styles = s.styles

    def add(self, begin, end, text):
        if text.startswith('[Script Info]'):
            self.setHeader(text)
        else:
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
        res.sort()
        while len(res) and res[0].end <= 0:
            logger.debug('removing subtitle line with negative time: %r', res[0])
            res.pop(0)
        return res

    def save(self, path, encoding=u'utf-8', fmt=None, fps=None, overwrite=False):
        if not overwrite and os.path.exists(path):
            logger.info('file "%s" exists, generating new path', path)
            path = genUniquePath(path)

        logger.info('saving subtitles to "%s", %s', path,
                utils.fmtstr(enc=encoding, fmt=fmt, fps=fps))

        try:
            if fmt is None:
                ext = os.path.splitext(path)[1].lower()
                fmts = [ x['type'] for x in filetypes.subtitleTypes if x['ext'] == ext ]
                if len(fmts):
                    fmt = fmts[0]
            if fmt is None:
                raise Exception(_('Unknown file extension'))

            with open(path, 'w', encoding=encoding, errors='replace') as fp:
                super().to_file(fp, format_=fmt, fps=fps)

        except Exception as e:
            raise error.Error(_('Can\'t save subtitle file') + '. ' + str(e)) \
                    .add('path', path) \
                    .add('encoding', encoding) \
                    .addn('format', fmt) \
                    .addn('fps', fps)

        return path

    def getMaxChange(self, formula):
        if len(self.events) > 0:
            return max(abs(formula.getY(x) - x) for x in
                    (self.events[0].start/1000.0, self.events[-1].end/1000.0))
        else:
            return 0.0


def genUniquePath(path):
    prefix, ext = os.path.splitext(path)
    if not prefix.endswith('.'):
        prefix += '.'

    i = 0
    while os.path.exists(path):
        i += 1
        path = '{}{}{}'.format(prefix, i, ext)

    return path


def isFpsBased(path):
    _, ext = os.path.splitext(path)
    fmt = pysubs2.formats.FILE_EXTENSION_TO_FORMAT_IDENTIFIER.get(ext)
    return fmt == 'microdvd'


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

