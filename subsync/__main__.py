#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

from subsync import translations
translations.init()

import wx
import sys
import argparse
from subsync import loggercfg
from subsync.settings import settings
from subsync.synchro import SyncTask, SyncTaskList, SubFile, RefFile, OutputFile, ChannelsMap


def subsync():
    from subsync.gui.errorwin import showExceptionDlg

    tasks, args = parseCmdArgs(sys.argv)
    app = wx.App()

    try:
        settings().load()
        translations.setLanguage(settings().language)

    except Exception as e:
        logger.warning('settings load failed, %r', e, exc_info=True)
        showExceptionDlg()

    setupLogger(args)

    if len(sys.argv) > 1:
        logger.info('command line parameters: %s', args)

    if args.window_size:
        settings().set(windowSize=args.window_size)

    try:
        from subsync.gui.mainwin import MainWin
        sub = tasks and tasks[0].sub
        ref = tasks and tasks[0].ref
        win = MainWin(None, sub=sub, ref=ref)
        win.Show()

        if tasks and args.auto:
            wx.CallAfter(win.start, task=tasks[0], auto=args.auto)

        app.MainLoop()

    except Exception as err:
        logger.warning('startup failed, %r', err, exc_info=True)
        showExceptionDlg()

    settings().save()
    loggercfg.terminate()


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


def parseCmdArgs(argv):
    parser = argparse.ArgumentParser(description=_('Subtitle Speech Synchronizer'))

    parser.add_argument('--sub', '--sub-file', type=str, help='subtitle file')
    parser.add_argument('--sub-stream', type=int, help='subtitle stream ID')
    parser.add_argument('--sub-lang', type=str, help='subtitle language')
    parser.add_argument('--sub-enc', type=str, help='subtitle character encoding')
    parser.add_argument('--sub-fps', type=float, help='subtitle framerate')

    parser.add_argument('--ref', '--ref-file', type=str, help='reference file')
    parser.add_argument('--ref-stream', type=int, help='reference stream ID')
    parser.add_argument('--ref-lang', type=str, help='reference language')
    parser.add_argument('--ref-enc', type=str, help='reference character encoding (for subtitle references)')
    parser.add_argument('--ref-fps', type=float, help='reference framerate')
    parser.add_argument('--ref-channels', type=str, help='reference channels mapping (for audio references)')

    parser.add_argument('--out', '--out-file', type=str, help='output file (used with --auto)')
    parser.add_argument('--out-fps', type=float, help='output framerate (for fps-based subtitles)')
    parser.add_argument('--out-enc', type=str, help='output character encoding')
    parser.add_argument('--effort', type=float, default=None, help='how hard to try (0.0 - 1.0)')

    parser.add_argument('--loglevel', type=str, help='set logging level, numerically or by name')
    parser.add_argument('--logfile', type=str, help='dump logs to specified file')

    parser.add_argument('--window-size', type=int, help='maximum timestamp adjustement (in seconds)')
    parser.add_argument('--auto', type=str, nargs='?', choices=['start', 'sync', 'done'],
            help='start synchronization automatically')

    args = parser.parse_args()
    tasks = None

    if args.sub or args.ref or args.out:
        task = SyncTask()

        if args.sub:
            task.sub = SubFile(path=args.sub)
            if args.sub_stream != None:
                task.sub.select(args.sub_stream - 1)
            task.sub.setNotNone(lang=args.sub_lang, enc=args.sub_enc, fps=args.sub_fps)

        if args.ref:
            task.ref = RefFile(path=args.ref)
            if args.ref_stream != None:
                task.ref.select(args.ref_stream - 1)
            task.ref.setNotNone(lang=args.ref_lang, enc=args.ref_enc, fps=args.ref_fps)

            if args.ref_channels != None:
                task.ref.channels = ChannelsMap.deserialize(args.ref_channels)

        if args.out:
            task.out = OutputFile(path=args.out, fps=args.out_fps, enc=args.out_enc)

        tasks = [ task ]

    if args.effort is not None:
        settings().set(minEffort = args.effort)

    return tasks, args


if __name__ == "__main__":
    subsync()

