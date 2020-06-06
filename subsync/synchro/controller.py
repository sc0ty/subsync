from collections import namedtuple
from typing import Iterable
import time
import threading
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
        self._semaphore = threading.Semaphore()
        self._sync = None
        self._terminated = False

    def configure(self, **options):
        for key, val in options.items():
            if key not in self._options:
                raise TypeError("Unexpected keyword argument '{}'".format(key))
            self._options[key] = val

    def synchronize(self, tasks, timeout=None):
        if self.isRunning():
            raise RuntimeError('Another synchronization in progress')

        logger.debug('synchronization options: %s', self._options)

        self._terminated = False
        if isinstance(tasks, Iterable):
            self._thread = threading.Thread(
                    target=self._run,
                    args=(tasks, timeout),
                    name='Synchronizer')
        else:
            self._thread = threading.Thread(
                    target=self._runTask,
                    args=(tasks, timeout),
                    name='Synchronizer')
        self._thread.start()

    def terminate(self):
        self._terminated = True
        self._semaphore.release()

    def isRunning(self):
        return self._thread and self._thread.is_alive()

    def wait(self):
        if self._thread:
            self._thread.join()
        return not self._terminated

    def getStatus(self):
        return self._sync and self._sync.getStatus()

    def getProgress(self):
        return self._sync and self._sync.getProgress()

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

    def _run(self, tasks, timeout):
        try:
            for no, task in enumerate(tasks):
                if not self._terminated:
                    logger.info('running task %i/%i: %r', no, len(tasks), task)
                    self._runTask(task, timeout)
                else:
                    break

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(None, 'core', err)

        finally:
            logger.info('synchronization finished')
            self._onFinish(self._terminated)

    def _runTask(self, task, timeout):
        try:
            self._onJobStart(task)
            self._sync = sync = Synchronizer(task.sub, task.ref)
            sync.onUpdate = self._semaphore.release
            sync.onError = lambda src, err: self._onError(task, src, err)

            sync.init(self._options, runCb=lambda: not self._terminated)
            if not self._terminated:
                sync.start()

            self._onJobInit(task)

            status = sync.getStatus()
            minEffort = self._options.get('minEffort', 1.0)
            if timeout is not None:
                lastTime = time.monotonic() - timeout

            while not self._terminated and sync.isRunning() \
                    and (minEffort >= 1.0 or status.effort < minEffort):
                self._semaphore.acquire(timeout=timeout)
                status = sync.getStatus()

                notify = False
                if timeout is None:
                    notify = True
                else:
                    now = time.monotonic()
                    if now - lastTime >= timeout:
                        lastTime = now
                        notify = True

                if notify:
                    self._onJobUpdate(task, status)

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(task, 'core', err)

        try:
            sync.stop(force=True)
            status = sync.getStatus()
            logger.info('result: %r', status)
            succeeded = not self._terminated and status and status.correlated
            path = None

            if succeeded and task.out:
                try:
                    path = self.saveSynchronizedSubtitles(task=task)

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
