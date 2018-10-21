import config
import utils
import thread
import pubkey
import error
import requests
import tempfile
import zipfile
import collections
import Crypto
import os
import sys

import logging
logger = logging.getLogger(__name__)


DownloaderState = collections.namedtuple('DownloaderState',
        ['action', 'progress', 'error', 'terminated'])


class Downloader(thread.Thread):
    def __init__(self, type=None, url=None, sig=None, version=None, size=None, **kw):
        super().__init__()
        self.type = type
        self.url = url
        self.sig = sig
        self.version = utils.parvseVersion(version)
        self.size = size
        self.fp = None
        self.hash = Crypto.Hash.SHA256.new()
        self.state = thread.AtomicValue()

    def run(self):
        yield from self.validate()
        yield from self.download()
        yield from self.verify()
        yield from self.install()

    def setState(self, action, progress=None, error=None, terminated=False):
        state = DownloaderState(action, progress, error, terminated)
        self.state.set(state)

    def getState(self):
        return self.state.get()

    def validate(self):
        for key, val in dict(type=self.type, url=self.url, sig=self.sig).items():
            if val == None:
                raise error.Error('Invalid asset data, missing parameter', key=key)
        yield

    def download(self):
        logger.info('downloading %s', self.url)
        self.setState('download')

        try:
            req = requests.get(self.url, stream=True)
            req.raise_for_status()
            self.fp = tempfile.SpooledTemporaryFile(max_size=64*1024*1024)
            yield

            pos = 0
            size = getSizeFromHeader(req.headers, self.size)

            for chunk in req.iter_content(8192):
                self.fp.write(chunk)
                self.hash.update(chunk)
                pos += len(chunk)
                self.setState('download', progress=(pos, size))
                yield

        except Exception as e:
            raise error.Error(_('Asset download failed'), details=str(e),
                type=self.type, url=self.url)

        logger.info('successfully downloaded %s', self.url)

    def verify(self):
        logger.info('verifying signature')
        self.setState('verify', progress=1.0)

        sig = None

        try:
            req = requests.get(self.sig)
            req.raise_for_status()
            sig = req.content

        except Exception as e:
            raise error.Error(_('Signature download failed'), details=str(e),
                type=self.type, url=self.sig)

        if not pubkey.getVerifier().verify(self.hash, sig):
            self.fp.close()
            self.fp = None
            raise error.Error(_('Signature verification failed'), url=self.url)
        yield

    def install(self):
        logger.info('installing %s', self.url)
        self.setState('install', progress=1.0)

        if self.type == 'zip':
            dstdir = config.assetdir
            logger.info('extracting zip asset to %s', dstdir)
            os.makedirs(dstdir, exist_ok=True)
            zipf = zipfile.ZipFile(self.fp)
            zipf.extractall(dstdir)

        else:
            raise error.Error('Invalid asset type', type=self.type, url=self.url)

        self.fp.close()
        self.fp = None
        yield

    def done(self):
        self.setState('done', progress=1.0, terminated=True)

    def error(self, err):
        self.setState('error', error=sys.exc_info(), terminated=True)


def getSizeFromHeader(headers, defaultSize=None):
    try:
        return int(headers.get('content-length'))
    except:
        return defaultSize

