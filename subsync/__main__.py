#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

from subsync import translations
translations.init()

import sys
from subsync import cmdargs
from subsync import loggercfg
from subsync.settings import settings


def subsync():
    args = cmdargs.parseCmdArgs()
    initConfig(args)

    if shouldUseCli():
        startCli(args)
    else:
        startGui(args)
        settings().save()

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


def shouldUseCli():
    if settings().cli:
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
    from subsync.gui.errorwin import showExceptionDlg

    try:
        app = wx.App()
        win = MainWin(None)

        win.Show()
        if settings().mode == 'batch':
            wx.CallLater(100, win.showBatchWin)

        app.MainLoop()

    except Exception as err:
        logger.error('subsync failed, %r', err, exc_info=True)
        showExceptionDlg()


def startCli(args):
    from subsync import cli

    try:
        app = cli.App(verbosity=args.verbose)
        app.runTasks()

    except Exception as err:
        logger.error('subsync failed, %r', err, exc_info=True)


if __name__ == "__main__":
    subsync()

