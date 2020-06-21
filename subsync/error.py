import collections
import gizmo
import traceback
import sys


class Error(Exception):
    def __init__(self, msg, task=None, **fields):
        super(Error, self).__init__(msg)
        self.message = msg
        self.fields = fields
        self.addTask(task)

    def __repr__(self):
        return '{}; {}'.format(str(self.message),
                '; '.join('{}: {}'.format(k, v) for k, v in self.fields.items()))

    def __str__(self):
        return '{}\n{}'.format(self.message,
                '\n'.join('{}:\t{}'.format(k, v) for k, v in self.fields.items()))

    def add(self, key, val):
        self.fields[key] = val
        return self

    def addn(self, key, val):
        if val != None:
            self.fields[key] = val
        return self

    def addTask(self, task):
        if task:
            self.addn('sub', task.sub)
            self.addn('ref', task.ref)
            self.addn('out', task.out)
        return self


class ErrorsGroup(object):
    def __init__(self, msg):
        self.message = msg
        self.descriptions = set()
        self.errors = []
        self.fields = collections.defaultdict(set)

    def add(self, err):
        self.errors.append(err)
        msg = None
        fields = []
        if type(err) is gizmo.Error:
            try:
                lines = str(err).split('\n')
                msg = lines[0]
                fields = [ v.strip().split(':', 1) for v in lines[1:] ]
            except:
                pass
        if hasattr(err, 'message'):
            msg = err.message
            self.descriptions.add(err.message)
        if hasattr(err, 'fields'):
            fields = err.fields.items()
        if not msg:
            msg = str(err) or repr(str)

        self.descriptions.add(msg)
        for key, val in fields:
            self.fields[key.strip()].add(val.strip())

    def __repr__(self):
        fields = [ ' - {}: {}'.format(k, formatFieldsVals(v))
                for k, v in sorted(self.fields.items()) ]

        return '{}\n{}\n{}'.format(
                self.message,
                '\n'.join(sorted(self.descriptions)),
                '\n'.join(fields))

    def __len__(self):
        return len(self.errors)


class ErrorsCollector(object):
    def __init__(self):
        self.groups = collections.OrderedDict()

    def __bool__(self):
        return bool(self.groups)

    def add(self, msg, src, err):
        if msg not in self.groups:
            self.groups[msg] = ErrorsGroup(msg)
        self.groups[msg].add(err)

    def getMessages(self, separator='\n'):
        msgs = [ err.message for err in self.groups.values() ]
        return separator.join(msgs)

    def getDetails(self):
        msgs = []
        for err in self.groups.values():
            msgs.append(err.message)
            msgs += list(err.descriptions)
            items = sorted(err.fields.items())
            msgs += [ '{}: {}'.format(k, formatFieldsVals(v, 10)) for k, v in items ]
            msgs.append('')
        return '\n'.join(msgs)


def formatFieldsVals(v, maxlen=4):
    res = '; '.join(sorted(v)[:maxlen])
    if len(v) > maxlen:
        res += ' ...'
    return res


def getExceptionMessage(e=None):
    if e is None:
        _, e, _ = sys.exc_info()

    if type(e) is gizmo.Error:
        return str(e).split('\n', 1)[0]
    elif type(e) is Error:
        return e.message
    else:
        return str(e) or repr(e)


def getExceptionDetails(excInfo=None):
    if excInfo:
        type, exc, tb = excInfo
    else:
        type, exc, tb = sys.exc_info()

    if exc:
        return ''.join(traceback.format_exception(type, exc, tb))


def getExceptionField(e, key):
    if type(e) is gizmo.Error:
        for line in str(e).split('\n'):
            ents = line.split(':', 1)
            if len(ents) == 2 and ents[0] == key:
                return ents[1].strip()
    elif type(e) is Error:
        return e.get(key)
