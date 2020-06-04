from threading import Thread
from collections import namedtuple
from typing import Iterable
import time
from .synchronizer import Synchronizer
from subsync.settings import settings

import logging
logger = logging.getLogger(__name__)


SyncJobResult = namedtuple('SyncJobResult', [ 'success', 'terminated', 'path' ])


class SyncController(object):
    def __init__(self, onJobStart=None, onJobInit=None, onJobEnd=None,
            onJobUpdate=None, onFinish=None, onError=None, listener=None):

        self._onJobStart = onJobStart or getattr(listener, 'onJobStart', lambda task: None)
        self._onJobInit = onJobInit or getattr(listener, 'onJobInit', lambda task: None)
        self._onJobEnd = onJobEnd or getattr(listener, 'onJobEnd', lambda task, status, result: None)
        self._onJobUpdate = onJobUpdate or getattr(listener, 'onJobUpdate', lambda task, status: None)
        self._onFinish = onFinish or getattr(listener, 'onFinish', lambda terminated: None)
        self._onError = onError or getattr(listener, 'onError', lambda task, source, error: None)

        self._options = settings().getSynchronizationOptions()
        self._thread = None
        self._sync = None

    def configure(self, **options):
        for key, val in options.items():
            if key not in self._options:
                raise TypeError("Unexpected keyword argument '{}'".format(key))
            self._options[key] = val

    def synchronize(self, tasks):
        if self.running():
            raise RuntimeError('Another synchronization in progress')

        self._terminated = False
        if isinstance(tasks, Iterable):
            self._thread = Thread(
                    target=self._run,
                    args=(tasks,),
                    name='Synchronizer')
        else:
            self._thread = Thread(
                    target=self._runTask,
                    args=(tasks,),
                    name='Synchronizer')
        self._thread.start()

    def terminate(self):
        self._terminated = True

    def running(self):
        return self._thread and self._thread.is_alive()

    def getSynchronizedSubtitles(self):
        if self._sync is None:
            raise RuntimeError('Subtitles not synchronized')
        return self._sync.getSynchronizedSubtitles()

    def saveSynchronizedSubtitles(self, path=None, task=None):
        if not path and not task:
            raise RuntimeError('At least one of the following arguments must be set: path or task')

        subs = self.getSynchronizedSubtitles()
        offset = self._options.get('outTimeOffset')
        if offset:
            logger.info('adjusting timestamps by offset %.3f', offset)
            subs.shift(s=offset)

        enc = (task and task.out and task.out.enc) \
                or self._options.get('outputCharEnc') \
                or (task and task.sub and task.sub.enc) or 'UTF-8'

        return subs.save(path=path or task.getOutputPath(),
                encoding=enc,
                fps=task and task.out and task.out.fps,
                overwrite=self._options.get('overwrite'))

    def _run(self, tasks):
        try:
            for no, task in enumerate(tasks):
                if not self._terminated:
                    logger.info('running task %i/%i: %r', task, len(tasks), task)
                    self._runTask(task)
                else:
                    res = SyncJobResult(False, True, None)
                    self._onJobEnd(task, None, res)

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(None, 'core', err)

        finally:
            logger.info('synchronization finished')
            self._onFinish(self._terminated)

    def _runTask(self, task):
        try:
            self._onJobStart(task)
            self._sync = sync = Synchronizer(task.sub, task.ref)
            sync.onError = lambda src, err: self._onError(task, src, err)

            sync.init(self._options, runCb=lambda: not self._terminated)
            if not self._terminated:
                sync.start()

            self._onJobInit(task)

            minEffort = self._options.get('minEffort', 1.0)
            effort = -1

            while not self._terminated and sync.isRunning() \
                    and (minEffort >= 1.0 or effort < minEffort):
                status = sync.getStatus()
                effort = status.effort
                self._onJobUpdate(task, status)
                time.sleep(0.5)

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(task, 'core', err)

        try:
            sync.stop(force=True)
            status = sync.getStatus()
            logger.info('result: %r', status)
            succeeded = not self._terminated and status and status.subReady
            path = None

            if succeeded and task.out:
                try:
                    path = self.saveSynchronizedSubtitle(task=task)

                except Exception as err:
                    logger.warning('subtitle save failed: %r', err, exc_info=True)
                    self._onError(task, 'core', err)
                    succeeded = False

            res = SyncJobResult(succeeded, self._terminated, path)
            self._onJobEnd(task, status, res)

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(task, 'core', err)

        finally:
            sync.destroy()
            logger.info('task finished %r', task)
