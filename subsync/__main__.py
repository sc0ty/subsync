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

    try:
        settings().load()
        translations.setLanguage(settings().language)

    except Exception as e:
        logger.warning('settings load failed, %r', e, exc_info=True)

    settings().set(**cmdargs.parseSettingsArgs(args))
    setupLogger(args)

    if len(sys.argv) > 1:
        logger.info('command line parameters: %s', args)

    if shouldUseCli(args):
        startCli(args)
    else:
        startGui(args)
        settings().save()

    loggercfg.terminate()


def shouldUseCli(args):
    if args.cli:
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

        if args.mode == 'sync':
            task = cmdargs.parseSyncArgs(args)
            win = MainWin(None, sub=task.sub, ref=task.ref)
            win.Show()

        elif args.mode == 'batch':
            tasks = cmdargs.parseBatchArgs(args)
            win = MainWin(None)
            win.Show()
            wx.CallAfter(win.showBatchWin, tasks=tasks)

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
        tasks = []
        if args.mode == 'sync':
            tasks = [ cmdargs.parseSyncArgs(args) ]
        elif args.mode == 'batch':
            tasks = cmdargs.parseBatchArgs(args)

        app = cli.App(verbosity=args.verbose)
        app.runTasks(tasks)

    except Exception as err:
        logger.error('subsync failed, %r', err, exc_info=True)


def setupLogger(args):
    level = parseLogLevel(args.loglevel)
    if level == None:
        level = settings().logLevel

    path = args.logfile
    if path == None:
        path = settings().logFile

    loggercfg.init(level=level, path=path)

    blacklist = settings().logBlacklist
    if blacklist:
        loggercfg.setBlacklistFilters(blacklist)


def parseLogLevel(level, default=logging.WARNING):
    for name in [ 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ]:
        if level == name:
            return getattr(logging, name)
    try:
        return int(level)
    except:
        return None


if __name__ == "__main__":
    subsync()

