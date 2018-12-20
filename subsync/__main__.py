#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

from subsync import translations
translations.init()

import wx
import sys
import argparse
from subsync import error
from subsync import loggercfg
from subsync.settings import settings
from subsync.stream import Stream
from subsync import channels


def subsync():
    from subsync.gui.errorwin import showExceptionDlg

    subs, refs, args = parseCmdArgs(sys.argv)
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
        win = MainWin(None, subs=subs, refs=refs)
        win.Show()

        if args.auto:
            autoRun(win, args)

        app.MainLoop()

    except error.Error as e:
        showExceptionDlg()

    settings().save()
    loggercfg.terminate()


def autoRun(mainWin, args):
    class Listener(object):
        def onSynchronized(self, win, stats):
            self.save(win, stats)
            if args.auto == 'sync':
                win.Close()

        def onSynchronizationDone(self, win, stats):
            self.save(win, stats)
            if args.auto in ['sync', 'done']:
                win.Close()

        def onSynchronizationExit(self, win):
            if args.auto in ['sync', 'done']:
                mainWin.Close()

        def save(self, win, stats):
            if args.out and stats.correlated:
                win.saveSynchronizedSubtitles(args.out, fps=args.out_fps)

    mainWin.start(Listener())


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
    subs = None
    refs = None

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

    parser.add_argument('--loglevel', type=str, help='set logging level, numerically or by name')
    parser.add_argument('--logfile', type=str, help='dump logs to specified file')

    parser.add_argument('--window-size', type=int, help='maximum timestamp adjustement (in seconds)')
    parser.add_argument('--auto', type=str, nargs='?', choices=['start', 'sync', 'done'],
            help='start synchronization automatically')

    args = parser.parse_args()

    if args.sub:
        subs = Stream(path=args.sub, types=('subtitle/text',))
        if args.sub_stream != None:
            subs.select(args.sub_stream - 1)
        subs.setNotNone(lang=args.sub_lang, enc=args.sub_enc, fps=args.sub_fps)

    if args.ref:
        refs = Stream(path=args.ref, types=('subtitle/text', 'audio'))
        if args.ref_stream != None:
            refs.select(args.ref_stream - 1)
        refs.setNotNone(lang=args.ref_lang, enc=args.ref_enc, fps=args.ref_fps)

        if args.ref_channels != None:
            refs.channels = channels.getChannelsMap(args.ref_channels)

    return subs, refs, args


if __name__ == "__main__":
    subsync()

