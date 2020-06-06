from subsync.synchro import SyncController
from subsync.assets import assetManager, assetListUpdater
from subsync.settings import settings
from subsync import utils
from subsync import error
import time
import threading

import logging
logger = logging.getLogger(__name__)


class Printer(object):
    def __init__(self, verbosity=1):
        self.lock = threading.Lock()
        self.verbosity = verbosity
        self.lineLen = 0

    def println(self, v, *args, **kwargs):
        if self.verbosity >= v:
            with self.lock:
                if self.lineLen:
                    print('', **kwargs)
                    self.lineLen = 0
                print(*args, **kwargs)

    def reprint(self, v, msg, **kwargs):
        if self.verbosity >= v:
            with self.lock:
                padding = ' ' * (len(msg) - self.lineLen)
                print('{}{}\r'.format(msg, padding), end='', flush=True, **kwargs)
                self.lineLen = len(msg)

    def printException(self, v, exc, msg=None):
        res = error.getExceptionMessage(exc)
        if msg:
            res = '{}: {}'.format(msg, res)
        self.println(v, '[!] ' + res.replace('\n', '\n[-] '))


pr = Printer()


class AssetsDownloader(object):
    def __init__(self, offline=False):
        self.gotAssetList = False
        self.offline = offline

    def getMissingAssets(self, task):
        needed = assetManager.getAssetsForTask(task)
        nonLocal= [ asset for asset in needed if not asset.isLocal() ]

        if nonLocal and not self.offline:
            self.downloadAssetList()

            missing = [ asset for asset in nonLocal if asset.isMissing() ]
            if missing:
                self.printMissingAssets(missing)
                return False

            for asset in nonLocal:
                if not self.downloadAsset(asset):
                    return False

            missing = [ asset for asset in needed if not asset.isLocal() ]
            if missing:
                self.printMissingAssets(missing)
                return False

        return True

    def printMissingAssets(self, assets):
        pr.println(0, '[!] there is no assets needed to perform synchronization')
        for asset in assets:
            pr.println(1, '[-] asset {} is missing'.format(asset.getPrettyName()))

    def downloadAssetList(self, force=False):
        if force or not self.gotAssetList:
            pr.println(1, '[+] updating asset list')
            assetListUpdater.startSynchronous(updateList=True, autoUpdate=False)
            self.gotAssetList = True

    def downloadAsset(self, asset):
        name = asset.getPrettyName()
        updater = asset.getUpdater()
        updater.start()

        while updater.isRunning():
            self.printDownloadStats(name, updater.getStatus())
            time.sleep(1)

        status = updater.getStatus()
        if status.state == 'done' and status.detail == 'success':
            self.printDownloadStats(name, status)
            return True
        else:
            pr.println(0, '[!] FAILED')
            if status.error:
                pr.printException(1, status.error[1])
                pr.println(2, error.getExceptionDetails(status.error))
            return False

    def printDownloadStats(self, name, status):
        pos, size = status.progress or (None, None)
        msg = [ '[+] downloading ', name ]
        if pos is not None and size:
            msg += [ ' {:3.0f}%'.format(100 * pos / size) ]
        if pos is not None:
            msg += [ ': ', utils.fileSizeFmt(pos) ]
        if size:
            msg += [ ' / ', utils.fileSizeFmt(size) ]

        if pr.verbosity >= 3:
            pr.println(1, ''.join(msg))
        else:
            pr.reprint(1, ''.join(msg))


class App(object):
    def __init__(self, verbosity=1, offline=False):
        pr.verbosity = verbosity
        self.assetsDownloader = AssetsDownloader(offline)

    def runTasks(self, tasks):
        if not tasks:
            pr.println(1, '[-] nothing to do')
            return 0

        self.startTime = time.monotonic()
        self.lastTime = -1000
        self.succeeded = 0
        sync = None

        try:
            validTasks = [ task for task in tasks if self.validate(task) ]
            readyTasks = [ task for task in validTasks if self.assetsDownloader.getMissingAssets(task) ]

            sync = SyncController(listener=self)
            sync.synchronize(readyTasks, timeout=1.0)
            sync.wait()

            if self.succeeded == len(tasks):
                return 0
            else:
                return 2

        except KeyboardInterrupt:
            pr.println(1, '[-] interrupted by user')
            sync and sync.terminate()
            return 1

    def onJobStart(self, task):
        pr.println(1, '[*] starting synchronization {}'.format(task.sub.path))
        pr.println(2, '[+] sub: {}'.format(task.sub))
        pr.println(2, '[+] ref: {}'.format(task.ref))
        pr.println(2, '[+] out: {}'.format(task.out))

    def onJobUpdate(self, task, status):
        self.printStats(status)

    def onJobEnd(self, task, status, result):
        if status and not result.terminated:
            self.printStats(status, force=True)
        if result.success:
            pr.println(1, '[+] done, saved to {}'.format(result.path))
            self.succeeded += 1
        elif not result.terminated:
            pr.println(0, '[-] couldn\'t synchronize!')
        pr.println(1, '')

    def validate(self, task):
        sub = task.sub
        ref = task.ref
        out = task.out

        fails = []
        if sub is None or not sub.path or sub.no is None:
            fails.append('subtitles not set')
        if ref is None or not ref.path or ref.no is None:
            fails.append('reference file not set')
        if out is None or not out.path:
            fails.append('output file not set')
        if sub.path == ref.path and sub.no == ref.no:
            fails.append('subtitles can\'t be the same as reference')
        if ref.type == 'audio' and not ref.lang:
            fails.append('select reference language')

        try:
            out.validateOutputPattern()
        except Exception as e:
            fails.append(str(e))

        if fails:
            pr.println(0, '[!] cannot synchronize task {}'.format(sub and sub.path))
            for fail in fails:
                pr.println(1, '[-] {}'.format(fail))
            pr.println(1, '')
            return False
        else:
            return True

    def printStats(self, status, force=False):
        if pr.verbosity >= 1:
            progress = status.progress
            effort = settings().minEffort
            if effort:
                progress = min(max(progress, status.effort / effort, 0), 1)

            msg = '[+] {}: progress {:3.0f}%, {} points'.format(
                    utils.timeStampFmt(time.monotonic() - self.startTime),
                    100 * progress,
                    status.points)
            if pr.verbosity >= 2:
                msg += ', correlation={:.2f}, formula={}, maxChange={}'.format(
                        100 * status.factor,
                        str(status.formula),
                        utils.timeStampFractionFmt(status.maxChange))

            if pr.verbosity >= 3:
                pr.println(1, msg)
            else:
                pr.reprint(1, msg)

    def onError(self, task, source, err):
        pr.printException(1, err, source)

