from subsync import config
from subsync import utils
from subsync import error
import json
import shutil
import os
import subprocess
import stat

import logging
logger = logging.getLogger(__name__)


class SelfUpdater(object):
    def getLocalUpdate():
        try:
            dirPath = os.path.join(config.assetdir, 'upgrade')
            if os.path.isdir(dirPath):
                path = os.path.join(dirPath, 'upgrade.json')
                with open(path, encoding='utf8') as fp:
                    update = json.load(fp)

                return dict(
                        version = utils.parseVersion(update['version']),
                        path = os.path.join(dirPath, update['install']),
                        cwd = dirPath)

        except Exception as e:
            logger.warning('read update info failed, %r', e, exc_info=True)
            removeLocalUpdate()

    def removeLocalUpdate():
        try:
            path = os.path.join(config.assetdir, 'upgrade')
            if os.path.isdir(path):
                logger.info('removing update from %s', path)
                shutil.rmtree(path, ignore_errors=True)

        except Exception as e:
            logger.error('cannot remove upgrade data from %s: %r', path, e)

    def installLocalUpdate():
        try:
            update = getLocalUpdate()
            path = update['path']

            logger.info('executing installer %s', path)
            mode = os.stat(path).st_mode
            if (mode & stat.S_IEXEC) == 0:
                os.chmod(path, mode | stat.S_IEXEC)
            subprocess.Popen(path, cwd=update['cwd'])

        except Exception as e:
            logger.error('cannot install update %s: %r', path, e)
            raise error.Error(_('Update instalation failed miserably'))
