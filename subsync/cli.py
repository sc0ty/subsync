from subsync.synchro import SyncController
from subsync.assets import assetManager
from subsync.settings import settings
from subsync import validator, utils, error
import time
import threading


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
        if isinstance(exc, error.Error):
            for key, val in exc.fields.items():
                self.println(v+1, '[-] {}: {}'.format(key, val))


pr = Printer()


class AssetsVerifier(object):
    def run(self, tasks):
        assets = assetManager.getAssetsForTasks(tasks)

        if assets.notInstalled():
            self.printMissingAssets(self.notInstalled())
            return False
        else:
            return True

    def printMissingAssets(self, assets):
        pr.println(0, '[!] there is no assets needed to perform synchronization')
        for asset in assets:
            pr.println(1, '[-] asset {} is missing'.format(asset.getPrettyName()))


class AssetsDownloader(AssetsVerifier):
    def run(self, tasks):
        self.updateAssetList()
        assets = assetManager.getAssetsForTasks(tasks)

        if assets.missing():
            self.printMissingAssets(assets.missing())
            return False

        return self.installAssets(assets.notInstalled()) \
                and self.installAssets(assets.hasUpdate())

    def updateAssetList(self):
        listUpdater = assetManager.getAssetListUpdater()
        if not listUpdater.isRunning() and not listUpdater.isUpdated():
            pr.println(2, '[+] updating assets list')
            listUpdater.run()
            listUpdater.wait()
        return listUpdater.isUpdated()

    def installAssets(self, assets):
        for asset in assets:
            downloader = asset.download(onUpdate=self.onUpdate, timeout=0.5)
            try:
                downloader.wait(reraise=True)

            except KeyboardInterrupt:
                downloader.terminate()
                raise

            except error.Error as err:
                pr.printException(0, err)
                return False
        return True

    def onUpdate(self, asset, pos=None, size=None, start=False):
        msg = [ '[+] downloading ', asset.getPrettyName() ]
        if pos is not None and size:
            msg += [ ' {:3.0f}%'.format(100 * pos / size) ]
        if pos is not None:
            msg += [ ': ', utils.fileSizeFmt(pos) ]
        if size:
            msg += [ ' / ', utils.fileSizeFmt(size) ]

        if start or pr.verbosity >= 3:
            pr.println(1, ''.join(msg))
        else:
            pr.reprint(1, ''.join(msg))


class App(object):
    def __init__(self, verbosity=1, offline=False):
        pr.verbosity = verbosity
        if offline:
            self.assetsDownloader = AssetsVerifier()
        else:
            self.assetsDownloader = AssetsDownloader()

    def runTasks(self, tasks):
        if not tasks:
            pr.println(1, '[-] nothing to do')
            return 0

        self.startTime = time.monotonic()
        self.lastTime = -1000
        self.succeeded = 0
        sync = None

        try:
            validator.validateTasks(tasks, outputRequired=True)
        except Exception as err:
            pr.printException(0, err)
            return 1

        try:
            if not self.assetsDownloader.run(tasks):
                return 2

            sync = SyncController(listener=self)
            sync.synchronize(tasks, timeout=1.0)
            sync.wait()

            if self.succeeded == len(tasks):
                return 0
            else:
                return 2

        except KeyboardInterrupt:
            pr.println(1, '[-] interrupted by user')
            sync and sync.terminate()
            return 1

        except error.Error as err:
            pr.printException(0, err)
            raise

    def onJobStart(self, task):
        pr.println(1, '[*] starting synchronization {}'.format(task.sub.path))
        pr.println(2, '[+] sub: {}'.format(task.sub))
        pr.println(2, '[+] ref: {}'.format(task.ref))
        pr.println(2, '[+] out: {}'.format(task.out))

    def onJobUpdate(self, task, status):
        self.printStats(status)

    def onJobEnd(self, task, status, result):
        if status and not result.terminated:
            self.printStats(status, finished=True)
        if result.success:
            pr.println(1, '[+] done, saved to {}'.format(result.path))
            self.succeeded += 1
        elif not result.terminated:
            pr.println(0, '[-] couldn\'t synchronize!')
        pr.println(1, '')

    def printStats(self, status, finished=False):
        if pr.verbosity >= 1:
            if finished:
                progress = 1.0
            else:
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
