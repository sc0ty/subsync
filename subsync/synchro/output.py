from subsync import utils
from subsync.error import Error
import os

import logging
logger = logging.getLogger(__name__)


class OutputFile(object):
    def __init__(self, path=None, enc='UTF-8', fps=None):
        self.path = path
        self.enc  = enc
        self.fps  = fps
        self.overwrite = False
        self.pathFormatter = None

    def getPath(self, sub, ref):
        if self.pathFormatter is None:
            self.pathFormatter = PathFormatter()
        return self.pathFormatter.format(self.path, sub, ref)

    def validateOutputPattern(self):
        validatePattern(self.path)

    def serialize(self):
        res = {}
        if self.path: res['path'] = self.path
        if self.enc:  res['enc'] = self.enc
        if self.fps:  res['fps'] = self.fps
        if self.overwrite: res['overwrite'] = True
        return res

    def deserialize(data):
        if data:
            path = data.get('path', None)
            enc = data.get('enc', 'UTF-8')
            fps = data.get('fps', None)

            res = OutputFile(path, enc, fps)
            res.overwrite = data.get('overwrite', False)
            return res

    def __repr__(self):
        return utils.fmtobj(self.__class__.__name__,
                path = self.path,
                enc = self.enc,
                fps = self.fps,
                overwrite = self.overwrite or None)

    def __str__(self):
        return utils.fmtstr(self.path,
                enc = self.enc,
                fps = self.fps,
                overwrite = self.overwrite)


class PathFormatter(object):
    def __init__(self):
        self.clearCache()

    def clearCache(self):
        self.d = {}
        self.cache = (None, None, None)

    def format(self, pattern, sub, ref):
        if pattern is None or sub is None or ref is None:
            return None

        cacheKey = (sub.path, sub.no, sub.lang, ref.path, ref.no, ref.lang)

        if self.cache[0] == cacheKey:
            if self.cache[1] == pattern:
                return self.cache[2]

        else:
            self.d = {}
            for prefix, item in [ ('sub_', sub), ('ref_', ref) ]:
                self.d[ prefix + 'path' ] = item.path
                self.d[ prefix + 'no'   ] = str(item.no + 1)
                self.d[ prefix + 'lang' ] = item.lang or ''
                self.d[ prefix + 'name' ] = os.path.splitext(item.getBaseName())[0]
                self.d[ prefix + 'dir'  ] = os.path.dirname(item.path)

        path = formatPattern(pattern, self.d)
        self.cache = (cacheKey, pattern, path)
        return path


def validatePattern(pattern):
    d = {}
    for prefix in [ 'sub_', 'ref_' ]:
        for name in [ 'path', 'no', 'lang', 'name', 'dir' ]:
            d[ prefix + name ] = ''
    formatPattern(pattern, d)


def formatPattern(pattern, formatter):
    try:
        return pattern.format(**formatter, **{
            'if': ConditionalFormatter(formatter),
            'if_not': ConditionalFormatter(formatter, inverted=True)
            })

    except KeyError as e:
        raise Error(_('Invalid output pattern, invalid keyword: {}').format(e),
                pattern=pattern)

    except Exception as e:
        raise Error(_('Invalid output pattern, {}').format(e), pattern=pattern)


class ConditionalFormatter(object):
    def __init__(self, items, inverted=False):
        self.items = items
        self.inverted = inverted

    def __format__(self, fmt):
        key, val = fmt.split(':', 1)
        if bool(self.items[key]) ^ self.inverted:
            return val
        else:
            return ''
