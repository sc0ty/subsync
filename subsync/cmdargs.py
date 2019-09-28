from subsync.settings import settings, wordsDumpIds
import argparse
import logging
import re


def parseCmdArgs(argv=None):
    args =  getParser().parse_args(argv)

    if args.mode == 'sync':
        parseSyncArgs(args)
    elif args.mode == 'batch':
        parseBatchArgs(args)

    return args


def parseSyncArgs(args):
    from subsync.synchro import SyncTask, SubFile, RefFile, OutputFile, ChannelsMap

    sub = SubFile(path=args.sub)
    if args.sub_stream is not None:
        sub.select(args.sub_stream - 1)
    sub.setNotNone(lang=args.sub_lang, enc=args.sub_enc, fps=args.sub_fps)

    ref = RefFile(path=args.ref)
    if args.ref_stream is not None:
        ref.select(args.ref_stream - 1)
    ref.setNotNone(lang=args.ref_lang, enc=args.ref_enc, fps=args.ref_fps)
    if args.ref_channels is not None:
        ref.channels = ChannelsMap.deserialize(args.ref_channels)

    out = args.out and OutputFile(path=args.out, fps=args.out_fps, enc=args.out_enc)
    task = SyncTask(sub, ref, out)
    settings().tasks = [ task ]
    return task


def parseBatchArgs(args):
    from subsync.synchro import SyncTaskList
    tasks = SyncTaskList.load(args.batch)
    settings().tasks = tasks
    return tasks


def getParser():
    parser = argparse.ArgumentParser(description=_('Subtitle Speech Synchronizer'))
    subparsers = parser.add_subparsers()
    parser.set_defaults(mode=None)
    parser.set_defaults(effort=None)

    sync = subparsers.add_parser('sync', help=_('synchronization'))
    sync.set_defaults(mode='sync')
    sync.add_argument('--sub', '--sub-file', required=True, type=str, help=_('path to subtitle file'))
    sync.add_argument('--sub-stream', type=int, help=_('subtitle stream ID'))
    sync.add_argument('--sub-lang', type=str, help=_('subtitle language'))
    sync.add_argument('--sub-enc', type=str, help=_('subtitle character encoding'))
    sync.add_argument('--sub-fps', type=float, help=_('subtitle framerate'))
    sync.add_argument('--ref', '--ref-file', required=True, type=str, help=_('path to reference file'))
    sync.add_argument('--ref-stream', type=int, help=_('reference stream ID'))
    sync.add_argument('--ref-lang', type=str, help=_('reference language'))
    sync.add_argument('--ref-enc', type=str, help=_('reference character encoding (for subtitle references)'))
    sync.add_argument('--ref-fps', type=float, help=_('reference framerate'))
    sync.add_argument('--ref-channels', type=str, help=_('reference audio channels mapping (for audio references)'))
    sync.add_argument('--out', '--out-file', type=str, help=_('output file path (used with --cli)'))
    sync.add_argument('--out-fps', type=float, help=_('output framerate (for fps-based subtitles)'))
    sync.add_argument('--out-enc', type=str, help=_('output character encoding'))
    sync.add_argument('--effort', dest='minEffort', type=float, help=_('how hard to try (0.0 - 1.0) (used with --cli)'))

    batch = subparsers.add_parser('batch', help=_('batch synchronization'))
    batch.set_defaults(mode='batch')
    batch.add_argument('batch', type=str, help=_('batch job yaml description'))
    batch.add_argument('--effort', dest='minEffort', type=float, help=_('how hard to try (0.0 - 1.0) (used with --cli)'))

    setup = subparsers.add_parser('settings', help=_('change default settings'))
    setup.set_defaults(mode='settings')
    setup.add_argument('--effort', dest='minEffor', type=float, help=_('how hard to try (0.0 - 1.0) (used with --cli)'))

    cli = parser.add_argument_group(_('headless options'))
    cli.add_argument('--cli', action='store_true', help=_('headless mode (command line only)'))
    cli.add_argument('--verbose', type=int, default=1, help=_('verbosity level for headless job'))

    sync = parser.add_argument_group(_('synchronization options'))
    addOption(sync, 'jobsNo', '--jobs', type=int, metavar='NO', help=_('number of synchronization jobs, 0 for auto'))
    addOption(sync, 'windowSize', type=float, metavar='SIZE', help=_('maximum correction (in seconds)'))
    addOption(sync, 'maxPointDist', type=float, metavar='DIST', help=_('maximum synchronization error (type: in seconds)'))
    addOption(sync, 'minPointsNo', type=int, metavar='NO', help=_('minimum synchronization points no'))
    addOption(sync, 'minWordProb', type=float, metavar='PROB', help=_('minimum speech recognition score (type: 0.0 - 1.0)'))
    addOption(sync, 'minWordLen', type=int, metavar='LEN', help=_('minimum number of letters for word to be used in synchronization'))
    addOption(sync, 'minCorrelation', type=float, metavar='CORRELATION', help=_('minimum correlation (type: 0.0 - 1.0)'))
    addOption(sync, 'minWordsSim', type=float, metavar='SIM', help=_('minimum words similarity for synchronization point (type: 0.0 - 1.0)'))

    class LogLevelAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if values in [ 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL' ]:
                setattr(args, self.dest, getattr(logging, values))
            else:
                try:
                    setattr(args, self.dest, int(values))
                except ValueError:
                    raise argparse.ArgumentError(self, 'unrecognized level {}'.format(values))

    class WordsDumpAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if ':' in values:
                src, path = values.split(':', 1)
            else:
                src, path = values, None
            if src not in wordsDumpIds:
                raise argparse.ArgumentError(self, 'unrecognized source {}, should be one of {}'.format(src, wordsDumpIds))
            res = getattr(args, self.dest, None) or []
            res.append((src, path))
            setattr(args, self.dest, res)

    dbg = parser.add_argument_group(_('debug options'))
    addOption(dbg, 'logLevel', '--loglevel', type=str, action=LogLevelAction, help=_('set logging level, '
        'numericall value or one of: DEBUG, INFO, WARNING, ERROR, CRITICAL'))
    addOption(dbg, 'logFile', '--logfile', type=str, help=_('dump logs to specified file'))
    addOption(dbg, 'dumpWords', type=str, metavar='SRC[:PATH]', action=WordsDumpAction,
            help=_('dump words to file, or to standard output if there is no PATH, SRC is one of: ' + ', '.join(wordsDumpIds)))

    return parser


def addOption(parser, name, option=None, **kw):
    if not option:
        recase = re.compile('([A-Z])')
        option = '--' + recase.sub(r'-\1', name).lower()
    if not 'dest' in kw:
        kw['dest'] = name
    parser.add_argument(option, **kw)
