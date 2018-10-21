#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

import wx
import sys
import argparse
import gettext
import error
import assets
import loggercfg
from settings import settings
from stream import Stream

from gui.errorwin import showExceptionDlg
from gui.mainwin import MainWin


def subsync():
    gettext.install('subsync')
    subs, refs, args = parseCmdArgs(sys.argv)
    app = wx.App()

    try:
        settings().load()
    except Exception as err:
        showExceptionDlg()

    setupLogger(args)

    if len(sys.argv) > 1:
        logger.info('command line parameters: %s', args)

    if args.window_size:
        settings().set(windowSize=args.window_size)

    assets.init(autoUpdate=settings().autoUpdate)

    try:
        win = MainWin(None, subs=subs, refs=refs)
        win.Show()

        if args.auto:
            win.onButtonStartClick(None)

        app.MainLoop()

    except error.Error as err:
        showExceptionDlg()

    settings().save()
    assets.terminate()
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
    subs = None
    refs = None

    parser = argparse.ArgumentParser(description=_('Subtitle Speech Synchronizer'))

    parser.add_argument('--sub', '--sub-file', type=str, help='subtitle file')
    parser.add_argument('--sub-stream', type=int, help='subtitle stream ID')
    parser.add_argument('--sub-lang', type=str, help='subtitle language')
    parser.add_argument('--sub-enc', type=str, help='subtitle character encoding')

    parser.add_argument('--ref', '--ref-file', type=str, help='reference file')
    parser.add_argument('--ref-stream', type=int, help='reference stream ID')
    parser.add_argument('--ref-lang', type=str, help='reference language')
    parser.add_argument('--ref-enc', type=str, help='reference character encoding (for subtitle references)')
    parser.add_argument('--ref-fps', type=float, help='reference framerate')

    parser.add_argument('--loglevel', type=str, help='set logging level, numerically or by name')
    parser.add_argument('--logfile', type=str, help='dump logs to specified file')

    parser.add_argument('--window-size', type=int, help='maximum timestamp adjustement (in seconds)')
    parser.add_argument('--auto', action='store_true', help='start synchronization automatically')

    args = parser.parse_args()

    if args.sub:
        subs = Stream(path=args.sub)
        if args.sub_stream != None:
            subs.select(args.sub_stream - 1)
        subs.setNotNone(lang=args.sub_lang, enc=args.sub_enc)

    if args.ref:
        refs = Stream(path=args.ref)
        if args.ref_stream != None:
            refs.select(args.ref_stream - 1)
        refs.setNotNone(lang=args.ref_lang, enc=args.ref_enc, fps=args.ref_fps)

    return subs, refs, args


if __name__ == "__main__":
    subsync()

