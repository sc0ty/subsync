#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

from subsync import translations
translations.init()

import sys, os
from subsync import cmdargs
from subsync import loggercfg
from subsync.settings import settings


def subsync(argv=None):
    try:
        args = cmdargs.parseCmdArgs(argv)
        initConfig(args)

        if shouldUseCli():
            startCli(args)
        else:
            startGui(args)
            settings().save()

    finally:
        loggercfg.terminate()


def initConfig(args):
    loggerInit = False
    if args.logLevel is not None or args.logFile is not None:
        loggercfg.init(level=args.logLevel, path=args.logFile)
        loggerInit = True

    try:
        settings().load()
    except Exception as e:
        logger.warning('settings load failed, %r', e, exc_info=True)

    s = { k: v for k, v in vars(args).items() if k in settings().keys() and v is not None }
    tempSettings = args.mode != 'settings'
    settings().set(temp=tempSettings, **s)

    if not loggerInit or args.logLevel != settings().logLevel or args.logFile != settings().logFile:
        loggercfg.init(level=settings().logLevel, path=settings().logFile)

    if settings().logBlacklist:
        loggercfg.setBlacklistFilters(settings().logBlacklist)

    translations.setLanguage(settings().language)

    if len(sys.argv) > 1:
        logger.info('command line parameters: %s', args)

    settings().save()


def shouldUseCli():
    if settings().cli:
        return True
    if os.path.basename(os.path.splitext(sys.argv[0])[0]) == 'subsync-cmd':
        return True
    try:
        import wx
        return False
    except Exception as e:
        logger.warning('couldn\'t start wx, falling back to headless mode, %r', e)
        return True


def startGui(args):
    import wx
    from subsync.gui.mainwin import MainWin
    from subsync.gui.batchwin import BatchWin
    from subsync.gui.errorwin import showExceptionDlg

    try:
        app = wx.App()
        win = None
        tasks = loadTasks(args)

        if settings().mode == 'batch':
            win = BatchWin(None, tasks)
        else:
            win = MainWin(None)

        win.Show()
        app.MainLoop()

    except Exception as err:
        logger.error('subsync failed, %r', err, exc_info=True)
        showExceptionDlg()


def startCli(args):
    from subsync import cli

    try:
        loadTasks(args)

    except Exception as err:
        ind = '!'
        for e in str(err).split('\n'):
            print('[{}] {}'.format(ind, e))
            ind = '-'
        sys.exit(2)

    try:
        app = cli.App(verbosity=args.verbose)
        app.runTasks()

    except Exception as err:
        logger.error('subsync failed, %r', err, exc_info=True)


def loadTasks(args):
    if args.mode == 'sync':
        return cmdargs.parseSyncArgs(args)
    elif args.mode == 'batch':
        return cmdargs.parseBatchArgs(args)


def version():
    try:
        from subsync.version import version, version_short
        return version_short, version
    except:
        return None, 'UNDEFINED'


if __name__ == "__main__":
    subsync()

