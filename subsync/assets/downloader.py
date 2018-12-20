from subsync import config
from subsync import utils
from subsync import pubkey
from subsync import error
import aiohttp
import tempfile
import zipfile
import Crypto
import os

import logging
logger = logging.getLogger(__name__)


class AssetDownloader(object):
    def __init__(self, type=None, url=None, sig=None, version=None, size=None, **kw):
        self.type = type
        self.url = url
        self.sig = sig
        self.version = utils.parseVersion(version)
        self.size = size

        for key, val in dict(type=type, url=url, sig=sig).items():
            if val == None:
                raise error.Error('Invalid asset data, missing parameter', key=key)

    async def download(self, progressCb=None):
        logger.info('downloading %s', self.url)
        async with aiohttp.ClientSession(read_timeout=None, raise_for_status=True) as session:
            async with session.get(self.url) as response:
                pos = 0
                size = getSizeFromHeader(response.headers, self.size)

                fp = tempfile.TemporaryFile()
                hash = Crypto.Hash.SHA256.new()

                async for chunk, _ in response.content.iter_chunks():
                    fp.write(chunk)
                    hash.update(chunk)
                    pos += len(chunk)

                    if progressCb:
                        progressCb((pos, size))

                logger.info('successfully downloaded %s', self.url)
                return fp, hash

    async def verify(self, hash):
        logger.info('downloading signature')
        async with aiohttp.ClientSession() as session:
            async with session.get(self.sig) as response:
                assert response.status == 200
                sig = await response.read()

        logger.info('verifying signature')
        if not pubkey.getVerifier().verify(hash, sig):
            raise error.Error(_('Signature verification failed'), url=self.url)

        logger.info('signature is valid')

    async def install(self, fp):
        if self.type == 'zip':
            dstdir = config.assetdir
            logger.info('extracting zip asset to %s', dstdir)
            os.makedirs(dstdir, exist_ok=True)
            zipf = zipfile.ZipFile(fp)
            zipf.extractall(dstdir)
            logger.info('extraction completed')

        else:
            raise error.Error('Invalid asset type', type=self.type, url=self.url)

        fp.close()


def getSizeFromHeader(headers, defaultSize=None):
    try:
        return int(headers.get('content-length', defaultSize))
    except:
        return defaultSize

