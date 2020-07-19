from subsync.data import descriptions
import textwrap
import sys


def parseCmdArgs(argv=None):
    argvReader = ArgvReader(argv or sys.argv)
    try:
        opts = parse(argvReader, options())
        if len(argvReader) > 0:
            raise Exception("unrecognized option '{}'".format(argvReader.peekKey()))
        return opts
    except Exception as e:
        print(str(e), file=sys.stderr)

def printHelp(argv=None):
    app = (argv or sys.argv or [ 'subsync' ])[0]
    print(_('Usage: {} [OPTIONS]').format(app))

    def printHelpFor(opts, prefix=''):
        for opt in opts:
            if type(opt) is dict:
                name = getOptionName(opt, withGroup=True)
                descr = descriptions.cmdopts.get(prefix + name)
                if descr:
                    msg = '  ' + formatOptArg(opt) + '  '
                    msg += ' ' * (30 - len(msg))
                    msg += descr
                    print(textwrap.fill(msg, width=80, subsequent_indent=' ' * 30))
                if 'opts' in opt:
                    printHelpFor(opt['opts'], prefix=name + '.')
            else:
                print('')
                print(opt)

    printHelpFor(options())


class ArgvReader(object):
    def __init__(self, argv):
        self.argv = argv[1:]
        self.offset = 0

    def __len__(self):
        return len(self.argv)

    def peekKey(self):
        if len(self.argv) > 0:
            return self.argv[0].split('=', 1)[0]

    def popKey(self):
        if len(self.argv) > 0:
            if self.offset:
                raise Exception("option '{}' doesn't allow an argument".format(self.argv[0]))
            arg = self.argv[0].split('=', 1)
            if len(arg) == 1:
                self.argv.pop(0)
            else:
                self.offset = len(arg[0]) + 1
            return arg[0]

    def popValue(self):
        if len(self.argv) == 0:
            raise Exception('last option requires an argument')
        res = self.argv.pop(0)[self.offset:]
        self.offset = 0
        return res


### Helper functions ###

def parse(argv, opts):
    res = {}
    while len(argv) > 0:
        key = argv.peekKey()
        opt = findOption(opts, key)
        if opt is None:
            break
        argv.popKey()
        parserFn = opt.get('parser', parseVar)
        readArgs = parserFn(argv, res, key, **opt)

    for opt in opts:
        if type(opt) is dict and opt.get('required'):
            name = getOptionName(opt)
            group = opt.get('group')
            r = res
            if group:
                r = res.get(group, {})
            if name not in r:
                raise Exception("missing required option '{}'".format(name))
    return res

def findOption(options, name):
    for opt in options:
        if type(opt) is dict:
            if 'alias' in opt:
                if name == opt['alias']:
                    return opt
            elif 'aliases' in opt:
                if name in opt['aliases']:
                    return opt
            elif name == '--' + opt['name']:
                return opt

def getOptionName(opt, withGroup=False):
    name = opt['name'].split('-')
    name = name[0] + ''.join([ n.capitalize() for n in name[1:] ])
    if withGroup and 'group' in opt:
        name = '{}.{}'.format(opt['group'], name)
    return name

def addOptionVal(res, opt, value):
    name = getOptionName(opt)
    group = opt.get('group')
    if group:
        res[group] = res.get(group, {})
        res = res[group]

    if opt.get('multiple'):
        if name not in res:
            res[name] = []
        res[name].append(value)
    else:
        if name in res:
            raise Exception("duplicated option '{}'".format(opt[name]))
        res[name] = value

def formatOptArg(opt):
    name = opt['name']
    descr = descriptions.cmdopts.get(name)
    args = opt.get('aliases') or [ opt.get('alias') or '--' + name ]

    arglong =  [ arg for arg in args if arg.startswith('--') or not arg.startswith('-') ]
    argshort = [ arg for arg in args if arg not in arglong ]
    res = ', '.join(argshort + arglong)

    if 'values' in opt:
        res += '={{{}}}'.format(','.join(opt['values']))

    elif opt.get('parser') in [ None, parseVar ]:
        val = opt.get('metavar') or args[0].split('-')[-1].upper()
        res += '=' + val

    return res


### Specialized parsers used in options ###

def parseConst(argv, res, key, value=True, **opt):
    addOptionVal(res, opt, value)
    return 0

def parseVar(argv, res, key, type=str, **opt):
    try:
        addOptionVal(res, opt, type(argv.popValue()))
    except ValueError:
        raise Exception("invalid argument for option '{}', expected {}"
                .format(key, getattr(type, '__name__', str(type))))
    return 1

def parseEnum(argv, res, key, values, **opt):
    val = argv.popValue()
    if val not in values:
        raise Exception(
                "illegal value for option '{}', valid values are: {}".format(key,
                    ', '.join([ "'{}'".format(v) for v in values ])))
    addOptionVal(res, opt, val)
    return 1

def parseCmd(argv, res, key, opts, **opt):
    no = len(argv)
    addOptionVal(res, opt, parse(argv, opts))
    return no - len(argv)

def parseWordsDump(argv, res, key, **opt):
    vals = argv.popValue().split(':', 1)
    src = vals[0]
    path = None
    if len(vals) == 2:
        path = vals[1]
    addOptionVal(res, opt, (src, path))


### Command line options ###

def options():
    return [
        _('General options:'),
        { 'name': 'help', 'parser': parseConst, 'aliases': ['--help', '-h'] },
        { 'name': 'version', 'parser': parseConst, 'aliases': ['--version', '-v'] },
        { 'group': 'options', 'name': 'language', 'alias': '--lang' },

        _('Headless options:'),
        { 'name': 'cli', 'parser': parseConst, 'aliases': ['--cli', '-c'] },
        { 'name': 'verbose', 'type': int },
        { 'name': 'offline', 'parser': parseConst },

        _('GUI options:'),
        { 'name': 'batch', 'parser': parseConst },

        _('Synchronization job:'),
        { 'name': 'sync', 'parser': parseCmd, 'alias': 'sync', 'multiple': True, 'opts': [
            { 'group': 'sub', 'name': 'path', 'aliases': ['--sub', '--sub-file', '-s'], 'metavar': 'PATH', 'required': True },
            { 'group': 'sub', 'name': 'stream', 'alias': '--sub-stream', 'type': int, 'metavar': 'NO' },
            { 'group': 'sub', 'name': 'streamByLang', 'alias': '--sub-stream-by-lang' },
            { 'group': 'sub', 'name': 'lang', 'alias': '--sub-lang' },
            { 'group': 'sub', 'name': 'enc', 'alias': '--sub-enc' },
            { 'group': 'sub', 'name': 'fps', 'alias': '--sub-fps', 'type': float },

            { 'group': 'ref', 'name': 'path', 'aliases': ['--ref', '--ref-file', '-r'], 'metavar': 'PATH', 'required': True },
            { 'group': 'ref', 'name': 'stream', 'alias': '--ref-stream', 'type': int, 'metavar': 'NO' },
            { 'group': 'ref', 'name': 'streamByType', 'alias': '--ref-stream-by-type', 'parser': parseEnum,
                'values': ['sub', 'audio'] },
            { 'group': 'ref', 'name': 'streamByLang', 'alias': '--ref-stream-by-lang' },
            { 'group': 'ref', 'name': 'lang', 'alias': '--ref-lang' },
            { 'group': 'ref', 'name': 'enc', 'alias': '--ref-enc' },
            { 'group': 'ref', 'name': 'fps', 'alias': '--ref-fps', 'type': float },
            { 'group': 'ref', 'name': 'channels', 'alias': '--ref-channels' },

            { 'group': 'out', 'name': 'path', 'alias': '--out', 'aliases': ['--out', '--out-file', '-o'] },
            { 'group': 'out', 'name': 'enc', 'alias': '--out-enc' },
            { 'group': 'out', 'name': 'fps', 'alias': '--out-fps', 'type': float },
        ]},

        _('Synchronization options:'),
        { 'name': 'fromFile', 'alias': '--import', 'metavar': 'PATH' },
        { 'group': 'options', 'name': 'minEffort', 'alias': '--effort', 'type': float },
        { 'group': 'options', 'name': 'overwrite', 'parser': parseConst },
        { 'group': 'options', 'name': 'jobsNo',          'type': int, 'aliases': ['--jobs', '-j'], 'metavar': 'NO' },
        { 'group': 'options', 'name': 'window-size',     'type': float },
        { 'group': 'options', 'name': 'max-point-dist',  'type': float },
        { 'group': 'options', 'name': 'min-points-no',   'type': int },
        { 'group': 'options', 'name': 'min-word-prob',   'type': float },
        { 'group': 'options', 'name': 'min-word-len',    'type': int },
        { 'group': 'options', 'name': 'min-correlation', 'type': float, 'metavar': 'COR' },
        { 'group': 'options', 'name': 'min-words-sim',   'type': float },
        { 'group': 'options', 'name': 'out-time-offset', 'type': float },

        _('Debug options:'),
        { 'group': 'options', 'name': 'logLevel', 'alias': '--loglevel', 'parser': parseEnum,
                'values': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] },
        { 'group': 'options', 'name': 'logFile', 'alias': '--logfile' },
        { 'group': 'options', 'name': 'dump-words', 'metavar': 'SRC[:PATH]', 'parser': parseWordsDump, 'multiple': True },
        { 'group': 'options', 'name': 'test', 'parser': parseConst },
]

