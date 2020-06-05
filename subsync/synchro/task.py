from subsync.synchro.input import SubFile, RefFile
from subsync.synchro.output import OutputFile
from subsync import utils
import yaml


class SyncTask(object):
    def __init__(self, sub=None, ref=None, out=None, data=None):
        self.sub = sub
        self.ref = ref
        self.out = out
        self.data = data

    def getOutputPath(self):
        return self.out and self.out.getPath(self.sub, self.ref)

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

