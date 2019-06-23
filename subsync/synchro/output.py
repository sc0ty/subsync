from subsync import utils
import os


class OutputFile(object):
    def __init__(self, path=None, enc='UTF-8', fps=None):
        self.path = path
        self.enc  = enc
        self.fps  = fps
        self.overwrite = False

    def getPath(self):
        path = self.path
        if not self.overwrite and os.path.exists(path):
            i = 0
            p = path
            prefix, ext = os.path.splitext(path)
            if not prefix.endswith('.'):
                prefix += '.'

            while os.path.exists(p):
                i += 1
                p = '{}{}{}'.format(prefix, i, ext)
            path = p

        return path

    def getBaseName(self):
        if self.path:
            return os.path.basename(self.path)

    def getDirectory(self):
        if self.path:
            return os.path.dirname(self.path)

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
        return utils.repr(self.__class__.__name__,
                path = self.path,
                enc = self.enc,
                fps = self.fps,
                overwrite = self.overwrite or None)
