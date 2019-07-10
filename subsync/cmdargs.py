import argparse
import re


def parseCmdArgs(argv=None):
    return getParser().parse_args(argv)


def parseSettingsArgs(args):
    vargs = vars(args)

    settings = { k: v for k, v in vargs.items() if k in settingOptionsDescription and v is not None }

    if args.effort is not None:
        settings['minEffort'] = args.effort
    if args.jobs is not None:
        settings['jobsNo'] = args.jobs or None

    return settings


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

    return SyncTask(sub, ref, out)


def parseBatchArgs(args):
    from subsync.synchro import SyncTaskList
    return SyncTaskList.load(args.batch)


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
    sync.add_argument('--effort', type=float, help=_('how hard to try (0.0 - 1.0) (used with --cli)'))

    batch = subparsers.add_parser('batch', help=_('batch synchronization'))
    batch.set_defaults(mode='batch')
    batch.add_argument('batch', type=str, help=_('batch job yaml description'))
    batch.add_argument('--effort', type=float, help=_('how hard to try (0.0 - 1.0) (used with --cli)'))

    cli = parser.add_argument_group(_('headless options'))
    cli.add_argument('--cli', action='store_true', help=_('headless mode (command line only)'))
    cli.add_argument('--verbose', type=int, default=1, help=_('verbosity level for headless job'))

    settings = parser.add_argument_group(_('synchronization options'))
    settings.add_argument('--window-size', type=int, help=_('maximum correction (in seconds)'))
    settings.add_argument('--jobs', type=int, help=_('number of synchronization jobs, 0 for auto'))

    recase = re.compile('([A-Z])')
    for name, (type, help) in settingOptionsDescription.items():
        option = '--' + recase.sub(r'-\1', name).lower()
        settings.add_argument(option, dest=name, type=type, help=help)

    dbg = parser.add_argument_group(_('debug options'))
    dbg.add_argument('--loglevel', type=str, help=_('set logging level, numerically or by name'))
    dbg.add_argument('--logfile', type=str, help=_('dump logs to specified file'))

    return parser


settingOptionsDescription = {
        'maxPointDist':   (float, _('maximum synchronization error (in seconds)')),
        'minPointsNo':    (int,   _('minimum synchronization points no')),
        'minWordProb':    (float, _('minimum speech recognition score (0.0 - 1.0)')),
        'minWordLen':     (int,   _('minimum number of letters for word to be used in synchronization')),
        'minCorrelation': (float, _('minimum correlation (0.0 - 1.0)')),
        'minWordsSim':    (float, _('minimum words similarity for synchronization point (0.0 - 1.0)')),
}
