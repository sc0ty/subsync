import logging
logger = logging.getLogger(__name__)


# workaround for crashing mimetypes bug https://bugs.python.org/issue38672
import mimetypes, os
try:
    mimetypes.init()
except Exception as e:
    logger.warning('mimetypes init failed, %r', e, exc_info=True)
    paths = []
    for path in mimetypes.knownfiles:
        try:
            if os.path.isfile(path):
                open(path)
                paths.append(path)
        except Exception as e:
            logger.warning('offending file %s: %r', path, e)

    mimetypes.init(paths)


import os
import aiohttp
import json
from subsync.error import Error


async def downloadRaw(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            checkResponseCode(url, response)
            return await response.read()


async def downloadJson(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            checkResponseCode(url, response)
            return await response.json(content_type=None)


async def downloadFileProgress(url, fp, size=None, chunkCb=None):
    async with aiohttp.ClientSession(read_timeout=None, raise_for_status=True) as session:
        async with session.get(url) as response:
            checkResponseCode(url, response)

            pos = 0
            try:
                size = int(response.headers.get('content-length', size))
            except:
                pass

            async for chunk, _ in response.content.iter_chunks():
                fp.write(chunk)
                pos += len(chunk)

                if chunkCb:
                    chunkCb(chunk, (pos, size))


def checkResponseCode(url, response):
    if response.status < 200 or response.status >= 300:
        code = response.status
        reason = response.reason
        raise Error(_('Got response {}: {}').format(code, reason),
                code=code, reason=reason, url=url)


async def readJsonFile(path):
    if os.path.isfile(path):
        with open(path, encoding='utf8') as fp:
            return json.load(fp)


async def writeJsonFile(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as fp:
        json.dump(data, fp, indent=4)
