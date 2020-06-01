maxDistInfo = _(
'''Max adjustement. Subtitle time will be changed no more than this value. Higher value will result in longer synchronization, but if you set this too low, synchronization will fail.''')

effortInfo = _(
'''How hard should I work to synchronize subtitles. Higher value will result with better synchronization, but it will take longer.''')

noLanguageSelectedQuestion = _(
'''Langauge selection is not mandatory, but could drastically improve synchronization accuracy.
Are you sure?''')


### SettingsWin ###

maxPointDistInfo = _(
'''Maximum acceptable synchronization error, in seconds. Synchronization points with error greater than this will be discarded.''')

minPointsNoInfo = _(
'''Minumum number of synchronization points. Should not be set too high because it could result with generating large number of false positives.''')

minWordLenInfo = _(
'''Minimum word length, in letters. Shorter words will not be used as synchronization points. Applies only to alphabet-based languages.''')

minWordSimInfo = _(
'''Minimum words similarity for synchronization points. Between 0.0 and 1.0.''')

minCorrelationInfo = _(
'''Minimum correlation factor, between 0.0 and 1.0. Used to determine synchronization result. If correlation factor is smaller than this, synchronization will fail.''')

minWordProbInfo = _(
'''Minimum speech recognition score, between 0.0 and 1.0. Words transcribed with smaller score will be rejected.''')

outTimeOffset = _(
'''Fix output subtitle timestamps by given offset, in seconds.''')

jobsNoInfo = _(
'''Number of concurrent synchronization threads.''')

preventSystemSuspendInfo = _(
'''Prevents system from going to sleep during synchronization.
It could not work on all platforms.''')


### Command line options ###

cmdopts = {
'help':                    _('display this help text and exit'),
'version':                 _('display version information and exit'),
'options.language':        _('set user interface language'),

'cli':                     _('run in headless mode (without GUI)'),
'verbose':                 _('verbosity level (0 - 3)'),

'batch':                   _('open batch processing window'),

'sync':                    _('begin synchronization job, can be repeated multiple times'),
'sync.sub.path':           _('path to subtitle file'),
'sync.sub.stream':         _('subtitle stream no'),
'sync.sub.streamByLang':   _('select subtitle stream by language'),
'sync.sub.lang':           _('subtitle language'),
'sync.sub.enc':            _('subtitle character encoding'),
'sync.sub.fps':            _('subtitle framerate (for FPS-based subtitles)'),
'sync.ref.path':           _('path to reference file'),
'sync.ref.stream':         _('reference stream no'),
'sync.ref.streamByType':   _('select reference stream by type'),
'sync.ref.streamByLang':   _('select reference stream by language'),
'sync.ref.lang':           _('reference language'),
'sync.ref.enc':            _('reference character encoding (for subtitle references)'),
'sync.ref.fps':            _('reference framerate'),
'sync.ref.channels':       _('reference audio channels mapping (for audio references)'),
'sync.out.path':           _('output file path or pattern'),
'sync.out.fps':            _('output framerate (for FPS-based subtitles)'),
'sync.out.enc':            _('output character encoding'),

'import':                  _('import list of tasks from YAML file'),
'options.minEffort':       _('how hard to try (0.0 - 1.0)'),
'options.overwrite':       _('overwrite existing files'),

'options.jobsNo':          jobsNoInfo + ' ' + _('0 for auto.'),
'options.windowSize':      maxDistInfo + ' ' + _('In seconds.'),
'options.maxPointDist':    maxPointDistInfo,
'options.minPointsNo':     minPointsNoInfo,
'options.minWordProb':     minWordProbInfo,
'options.minWordLen':      minWordLenInfo,
'options.minCorrelation':  minCorrelationInfo,
'options.minWordsSim':     minWordSimInfo,
'options.outTimeOffset':   outTimeOffset,

'options.logLevel':        _('set logging level'),
'options.logFile':         _('dump logs to specified file'),
'options.dumpWords':       _('dump words to file, or to standard output if there is no PATH, SRC is one of:  ') + \
        ', '.join([ 'sub', 'subPipe', 'subRaw', 'ref', 'refPipe', 'refRaw' ])
}
