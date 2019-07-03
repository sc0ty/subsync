import argparse
from subsync.settings import settings
from subsync.synchro import SyncTask, SyncTaskList, SyncMode, SubFile, RefFile, OutputFile, ChannelsMap


def parseCmdArgs(argv=None):
    parser = getParser()
    args = parser.parse_args(argv)
    vargs = vars(args)

    settingKeys = set( s[0] for s in settingsArgs )
    newSettings = { k: v for k, v in vargs.items() if k in settingKeys and v is not None }

    if args.effort is not None:
        newSettings['minEffort'] = args.effort
    if args.jobs is not None:
        newSettings['jobsNo'] = args.jobs or None

    if newSettings:
        settings().set(**newSettings)

    mode = SyncMode(
            mode = vargs.get('mode', None),
            autoStart = not vargs.get('no_start', False),
            autoClose = not vargs.get('no_close', False))

    return mode, args


def parseSyncArgs(args):
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

    out = OutputFile(path=args.out, fps=args.out_fps, enc=args.out_enc)

    return SyncTask(sub, ref, out)


def parseBatchArgs(args):
    return SyncTaskList.load(args.batch)


def parseSyncMode(args):
    vargs = vars(args)


def getParser():
    parser = argparse.ArgumentParser(description=_('Subtitle Speech Synchronizer'))
    subparsers = parser.add_subparsers()
    parser.set_defaults(mode=None)
    parser.set_defaults(effort=None)

    sync = subparsers.add_parser('sync', help=_('synchronization'))
    sync.set_defaults(mode='sync')
    sync.add_argument('--sub', '--sub-file', required=True, type=str, help='subtitle file')
    sync.add_argument('--sub-stream', type=int, help='subtitle stream ID')
    sync.add_argument('--sub-lang', type=str, help='subtitle language')
    sync.add_argument('--sub-enc', type=str, help='subtitle character encoding')
    sync.add_argument('--sub-fps', type=float, help='subtitle framerate')
    sync.add_argument('--ref', '--ref-file', required=True, type=str, help='reference file')
    sync.add_argument('--ref-stream', type=int, help='reference stream ID')
    sync.add_argument('--ref-lang', type=str, help='reference language')
    sync.add_argument('--ref-enc', type=str, help='reference character encoding (for subtitle references)')
    sync.add_argument('--ref-fps', type=float, help='reference framerate')
    sync.add_argument('--ref-channels', type=str, help='reference channels mapping (for audio references)')
    sync.add_argument('--out', '--out-file', type=str, help='output file')
    sync.add_argument('--out-fps', type=float, help='output framerate (for fps-based subtitles)')
    sync.add_argument('--out-enc', type=str, help='output character encoding')
    sync.add_argument('--effort', type=float, help='how hard to try (0.0 - 1.0)')
    sync.add_argument('--no-start', action='store_true',
            help='don\'t start synchronization automatically (ignored with --cli)')
    sync.add_argument('--no-close', action='store_true',
            help='don\'t close application after synchronization (ignored with --cli)')

    batch = subparsers.add_parser('batch', help=_('batch synchronization'))
    batch.set_defaults(mode='batch')
    batch.add_argument('batch', type=str, help='batch job yaml description')
    batch.add_argument('--effort', type=float, help='how hard to try (0.0 - 1.0)')
    batch.add_argument('--no-start', action='store_true',
            help='don\'t start synchronization automatically (ignored with --cli)')
    batch.add_argument('--no-close', action='store_true',
            help='don\'t close application after synchronization (ignored with --cli)')

    cli = parser.add_argument_group(_('headless options'))
    cli.add_argument('--cli', action='store_true', help='headless mode (command line only)')
    cli.add_argument('--verbose', type=int, default=1, help='verbosity level for headless job')

    settings = parser.add_argument_group(_('synchronization options'))
    settings.add_argument('--window-size', type=int, help='maximum timestamp adjustement (in seconds)')
    settings.add_argument('--jobs', type=int, help='number of synchronization jobs, 0 for auto')

    for name, option, type, help in settingsArgs:
        settings.add_argument(option, dest=name, type=type, help=help)

    dbg = parser.add_argument_group(_('debug options'))
    dbg.add_argument('--loglevel', type=str, help='set logging level, numerically or by name')
    dbg.add_argument('--logfile', type=str, help='dump logs to specified file')

    return parser


settingsArgs = [
        ('maxPointDist', '--max-point-dist', float, ''),
        ('minPointsNo', '--min-points-no', int, ''),
        ('minWordProb', '--min-word-prob', float, ''),
        ('minWordLen', '--min-word-len', int, ''),
        ('minCorrelation', '--min-correlation', float, ''),
        ('minWordsSim', '--min-words-sim', float, '')
        ]
