from subsync.synchro.input import SubFile, RefFile
from subsync.synchro.output import OutputFile
from subsync.settings import settings
from subsync import utils
from collections import namedtuple
import yaml


class SyncTask(object):
    def __init__(self, sub=None, ref=None, out=None):
        self.sub = sub
        self.ref = ref
        self.out = out

    def getOutputPath(self):
        return self.out and self.out.getPath(self.sub, self.ref)

    def getOutputEnc(self):
        return (self.out and self.out.enc) or settings().outputCharEnc or \
                (self.sub and self.sub.enc) or 'UTF-8'

    def serialize(self):
        res = {}
        if self.sub: res['sub'] = self.sub.serialize()
        if self.ref: res['ref'] = self.ref.serialize()
        if self.out: res['out'] = self.out.serialize()
        return res

    def deserialize(data):
        if data:
            sub = SubFile.deserialize(data.get('sub'))
            ref = RefFile.deserialize(data.get('ref'))
            out = OutputFile.deserialize(data.get('out'))
            res = SyncTask(sub, ref, out)
            return res

    def __repr__(self):
        return utils.fmtobj(self.__class__.__name__,
                sub = repr(self.sub),
                ref = repr(self.ref),
                out = repr(self.out),
                )


class SyncTaskList(object):
    def deserialize(data):
        return [ SyncTask.deserialize(d) for d in data ]

    def load(path):
        with open(path, 'r') as fp:
            data = yaml.safe_load(fp)
        return SyncTaskList.deserialize(data)

    def save(tasks, path):
        data = [ task.serialize() for task in tasks ]
        with open(path, 'w') as fp:
            yaml.dump(data, fp, default_flow_style=False)

    def parseArgs(args):
        tasks = []
        if 'sub' in args or 'ref' in args or 'out' in args:
            tasks.append(SyncTask.deserialize({
                    'sub': args.get('sub'),
                    'ref': args.get('ref'),
                    'out': args.get('out'),
            }))
        if 'sync' in args:
            tasks += [ SyncTask.deserialize(sync) for sync in args['sync'] ]
        if 'import' in args:
            tasks += SyncTaskList.load(args['import'])
        return tasks

