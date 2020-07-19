from subsync.translations import _
from subsync.error import Error


def validateTask(task, outputRequired=False):
    sub, ref, out = task.sub, task.ref, task.out
    if sub is None or not sub.path or sub.no is None:
        raise Error(_('Subtitles not set'), task=task)
    if ref is None or not ref.path or ref.no is None:
        raise Error(_('Reference file not set'), task=task)
    if outputRequired and (not out or not out.path):
        raise Error(_('Output file not set'), task=task)
    if sub.path == ref.path and sub.no == ref.no:
        raise Error(_('Subtitles can\'t be the same as reference'), task=task)
    if ref.type == 'audio' and not ref.lang:
        raise Error(_('Select reference language first'), task=task)
    if out and out.path:
        try:
            out.validateOutputPattern()
        except:
            raise Error(_('Invalid output pattern'), task=task)


def validateTasks(tasks, outputRequired=False):
    for task in tasks:
        validateTask(task, outputRequired=outputRequired)
