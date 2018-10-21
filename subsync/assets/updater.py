import config
import utils
import json
import shutil
import os
import subprocess
import stat

import logging
logger = logging.getLogger(__name__)


class Updater(object):
    def __init__(self):
        self.upgradeReady = False
        self.install = None
        self.version = None
        self.load()

    def load(self):
        dirPath = os.path.join(config.assetdir, 'upgrade')
        path = os.path.join(dirPath, 'upgrade.json')

        if os.path.isdir(dirPath):
            try:
                with open(path, encoding='utf8') as fp:
                    upgrade = json.load(fp)

                self.install = os.path.join(dirPath, upgrade['install'])
                self.version = utils.parvseVersion(upgrade['version'])

                currentVersion = utils.getCurrentVersion()
                if currentVersion and self.version > currentVersion:
                    self.upgradeReady = True
                else:
                    self.upgradeReady = False
                    self.remove()

            except Exception as e:
                logger.error('invalid upgrade description, %r', e)
                self.remove()

    def remove(self):
        self.upgradeReady = False
        path = os.path.join(config.assetdir, 'upgrade')
        try:
            shutil.rmtree(path, ignore_errors=True)
        except Exception as e:
            logger.error('cannot remove upgrade data from %s: %r', path, e)

    def upgrade(self):
        cwd = os.path.join(config.assetdir, 'upgrade')
        path = os.path.join(cwd, self.install)
        logger.info('executing installer %s', path)

        mode = os.stat(path).st_mode
        if (mode & stat.S_IEXEC) == 0:
            os.chmod(path, mode | stat.S_IEXEC)
        subprocess.Popen(path, cwd=cwd)
        self.upgradeReady = False

