from subsync.synchro.input import SubFile, RefFile
from subsync.synchro.output import OutputFile
from subsync import utils
import yaml

__pdoc__ = { 'SyncTaskList': False }


class SyncTask(object):
    """Synchronization task."""

    def __init__(self, sub=None, ref=None, out=None, data=None):
        """
        Parameters
        ----------
        sub: subsync.SubFile or subsync.InputFile or dict
            Input subtitle file description. Proper object instance or `dict`
            with fields same as arguments to `subsync.InputFile`.
        ref: subsync.RefFile or subsync.InputFile or dict
            Reference file description. Proper object instance or `dict` with
            fields same as arguments to `subsync.InputFile`.
        out: subsync.OutputFile or dict
            Output subtitle file description. Proper object instance or `dict`
            with fields same as arguments to `subsync.OutputFile`.
        data: any, optional
            Any user defined data, useful for passing extra information via
            `subsync.SyncController` callbacks.
        """

        if isinstance(sub, dict): sub = SubFile(**sub)
        if isinstance(ref, dict): ref = RefFile(**ref)
        if isinstance(out, dict): out = OutputFile(**out)
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

    def __repr__(self):
        return utils.fmtobj(self.__class__.__name__,
                sub = repr(self.sub),
                ref = repr(self.ref),
                out = repr(self.out),
                )


class SyncTaskList(object):
    def deserialize(data):
        return [ SyncTask(**d) for d in data ]

    def load(path):
        with open(path, 'r') as fp:
            data = yaml.safe_load(fp)
        return SyncTaskList.deserialize(data)

    def save(tasks, path):
        data = [ task.serialize() for task in tasks ]
        with open(path, 'w') as fp:
            yaml.dump(data, fp, default_flow_style=False)
