from subsync.synchro import Synchronizer
from subsync.assets import assetManager, assetListUpdater
from subsync.settings import settings
from subsync import utils
from subsync import error
from time import sleep

import logging
logger = logging.getLogger(__name__)


class Printer(object):
    def __init__(self, verbosity=1):
        self.verbosity = verbosity
        self.lineTerminated = True

    def println(self, v, *args, **kwargs):
        if self.verbosity >= v:
            if not self.lineTerminated:
                self.lineTerminated = True
                print('')
            print(*args, **kwargs)

    def reprint(self, v, msg, endline=False):
        if self.verbosity >= v:
            print('\r{}        '.format(msg), end='')
            if endline:
                print('')
            self.lineTerminated = endline


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
            sleep(1)

        status = updater.getStatus()
        if status.state == 'done' and status.detail == 'success':
            self.printDownloadStats(name, status, endline=True)
            return True
        else:
            pr.println(0, '[!] FAILED')
            if status.error:
                pr.println(1, '[!] {}'.format(error.getExceptionMessage(status.error[1])))
                pr.println(2, error.getExceptionDetails(status.error))
            return False

    def printDownloadStats(self, name, status, endline=False):
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
            pr.reprint(1, ''.join(msg), endline)


class App(object):
    def __init__(self, verbosity=1, offline=False):
        pr.verbosity = verbosity
        self.assetsDownloader = AssetsDownloader(offline)

    def runTasks(self, tasks):
        if not tasks:
            pr.println(1, '[-] nothing to do')
            return 0

        succeeded = 0
        errors = 0

        for task in tasks:
            try:
                pr.println(1, '[*] starting synchronization {}'.format(task.sub.path))
                pr.println(2, '[+] sub: {}'.format(task.sub))
                pr.println(2, '[+] ref: {}'.format(task.ref))
                pr.println(2, '[+] out: {}'.format(task.out))

                if not self.validate(task):
                    continue

                if not self.assetsDownloader.getMissingAssets(task):
                    continue

                if self.synchronize(task):
                    succeeded += 1

            except KeyboardInterrupt:
                pr.println(1, '[-] interrupted by user')
                break

            except Exception as err:
                errors += 1
                logger.error('task: %r', task)
                logger.error('task failed, %r', err, exc_info=True)

        if errors:
            return 1
        if len(tasks) == succeeded:
            return 0
        else:
            return 2

    def validate(self, task):
        sub = task.sub
        ref = task.ref
        out = task.out

        if sub is None or not sub.path or sub.no is None:
            pr.println(0, '[!] subtitles not set')
            return False
        if ref is None or not ref.path or ref.no is None:
            pr.println(0, '[!] reference file not set')
            return False
        if out is None or not out.path:
            pr.println(0, '[!] output file not set')
            return False
        if sub.path == ref.path and sub.no == ref.no:
            pr.println(0, '[!] subtitles can\'t be the same as reference')
            return False
        if ref.type == 'audio' and not ref.lang:
            pr.println(0, '[!] select reference language')
            return False

        try:
            out.validateOutputPattern()
            return True

        except Exception as e:
            pr.println(0, '[!] {!s}'.format(e))
            return False

    def synchronize(self, task):
        sync = Synchronizer(task.sub, task.ref)
        try:
            sync.onError = self.onError

            sync.init(settings().getSynchronizationOptions())
            sync.start()

            effort = -1
            while sync.isRunning() and effort < settings().minEffort:
                status = sync.getStatus()
                effort = status.effort
                self.printStats(status)
                sleep(1)

            sync.stop()
            status = sync.getStatus()

            if status and status.subReady:
                self.printStats(status, endline=True)
                path = task.getOutputPath()
                pr.println(1, '[+] saving to {}'.format(path))

                try:
                    npath = sync.getSynchronizedSubtitles().save(
                            path=path,
                            encoding=task.getOutputEnc(),
                            fps=task.out.fps,
                            overwrite=settings().overwrite)

                    if path != npath:
                        pr.println(1, '[+] file exists, saving to {}'.format(npath))

                    pr.println(1, '[+] done')
                    return True

                except error.Error as e:
                    pr.println(0, '[!] {}'.format(error.getExceptionMessage(e)))
                    raise

            else:
                pr.println(0, '[-] couldn\'t synchronize!')
                return False

        finally:
            sync.destroy()

    def printStats(self, status, endline=False):
        if pr.verbosity >= 1:
            progress = status.progress
            effort = settings().minEffort
            if effort:
                progress = min(max(progress, status.effort / effort, 0), 1)

            msg = '[+] synchronization {:3.0f}%: {} points'.format(100 * progress, status.points)
            if pr.verbosity >= 2:
                msg += ', correlation={:.2f}, formula={}, maxChange={}'.format(
                        100 * status.factor,
                        str(status.formula),
                        utils.timeStampFractionFmt(status.maxChange))

            if pr.verbosity >= 3:
                pr.println(1, msg)
            else:
                pr.reprint(1, msg, endline)


    def onError(self, source, err):
        pr.println(2, source, err)
