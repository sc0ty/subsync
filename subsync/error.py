import collections
import gizmo
import error

import logging
logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, msg, **fields):
        super(Error, self).__init__(msg)
        self.message = msg
        self.fields = fields

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


class ErrorsGroup(object):
    def __init__(self, msg):
        self.message = msg
        self.descriptions = set()
        self.errors = []
        self.fields = collections.defaultdict(set)

    def add(self, error):
        self.errors.append(error)
        if hasattr(error, 'message'):
            self.descriptions.add(error.message)
        if hasattr(error, 'fields'):
            for key, val in error.fields.items():
                self.fields[key].add(val)

    def __repr__(self):
        fields = [ ' - {}: {}'.format(k, formatFieldsVals(v))
                for k, v in sorted(self.fields.items()) ]

        return '{}\n{}\n{}'.format(
                self.message,
                '\n'.join(sorted(self.descriptions)),
                '\n'.join(fields))

    def __len__(self):
        return len(self.errors)


def formatFieldsVals(v, maxlen=4):
    res = '; '.join(sorted(v)[:maxlen])
    if len(v) > maxlen:
        res += ' ...'
    return res


def getExceptionMessage(e):
    if type(e) is gizmo.Error:
        return str(e).split('\n', 1)[0]
    elif type(e) is error.Error:
        return e.message
    else:
        return str(e)

