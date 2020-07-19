from collections import namedtuple
from typing import Iterable
import time
import threading
from subsync.settings import settings
from subsync.error import Error

import logging
logger = logging.getLogger(__name__)


__pdoc__ = {
        'SyncJobResult.success': 'Whether synchronization succeeded.',
        'SyncJobResult.terminated': 'Whether synchronization was terminated with `SyncController.terminate`.',
        'SyncJobResult.path': 'Where output subtitles was saved. `None` if subtites was not saved automatically.',

        'SyncStatus.correlated': 'Whether subtitles are correlated and ready to be saved.',
        'SyncStatus.maxChange': 'Maximum time delta that was applied for a single subtitle line, in seconds.',
        'SyncStatus.progress': 'Progress estimation, between 0 and 1.',
        'SyncStatus.factor': 'Correlation factor, between 0 and 1.',
        'SyncStatus.points': 'Number of synchronization points.',
        'SyncStatus.formula': 'Mathematical formula used for synchronization.',
        'SyncStatus.effort': 'Current effort spent for synchronization, between 0 and 1 or -1 if not yet correlated.',
        }


SyncJobResult = namedtuple('SyncJobResult', [
    'success',
    'terminated',
    'path',
    ])
SyncJobResult.__doc__ = """Result of single synchronization task."""


SyncStatus = namedtuple('SyncStatus', [
    'correlated',
    'maxChange',
    'progress',
    'factor',
    'points',
    'formula',
    'effort',
])
SyncStatus.__doc__ = """Synchronization status.

Notes
-----
`correlated` set to `True` does not necessary mean that correlation is done -
we could yet get better fix.
In interactive mode, subtitles could be saved when `correlated` is set.
"""


class SyncController(object):
    """Synchronization controller.

    Controls subtitle synchronization process. Synchronization is performed
    asynchronously in separate threads controlled internally. Status is reported
    by optional callbacks.
    """

    def __init__(self, listener=None, **kw):
        """
        Parameters
        ----------
        listener: object, optional
            Object with methods named as following callback parameters.
        onJobStart: callable(task), optional
            Called when the task synchronization starts.
        onJobEnd: callable(task, status, result), optional
            Called when the task synchronization ends.
        onJobUpdate: callable(task, status), optional
            Called periodically during synchronization to report current state.
        onFinish: callable(terminated), optional
            Called when synchronizer ends its work - either all tasks are
            processed or synchronization was terminated;
        onError: callable(task, source, error), optional
            Called to report non-terminal errors. Non-terminal errors are errors
            not causing synchronizer to stop, but could impact results, e.g. audio
            decoding errors.

        Notes
        -----
        Callbacks arguments:

        - task : `subsync.synchro.SyncTask` - object passed to
            `SyncController.synchronize`;
        - status : `SyncStatus` - object reflecting current synchronization state;
        - result : `SyncJobResult`;
        - terminated : `bool` - whether synchronization was terminated;
        - source : `str` - error source, could be 'sub' or 'ref' for
            subtitle/reference extractor or 'core';
        - error - exception instance.
        """
        self._onJobStart = kw.get('onJobStart', getattr(listener, 'onJobStart', lambda task: None))
        self._onJobInit = kw.get('onJobInit', getattr(listener, 'onJobInit', lambda task: None))
        self._onJobEnd = kw.get('onJobEnd', getattr(listener, 'onJobEnd', lambda task, status, result: None))
        self._onJobUpdate = kw.get('onJobUpdate', getattr(listener, 'onJobUpdate', lambda task, status: None))
        self._onFinish = kw.get('onFinish', getattr(listener, 'onFinish', lambda terminated: None))
        self._onError = kw.get('onError', getattr(listener, 'onError', lambda task, source, error: None))

        self._options = settings().getSynchronizationOptions()
        self._thread = None
        self._semaphore = threading.Semaphore()
        self._sync = None
        self._terminated = False

    def configure(self, **kw):
        """Override default synchronization options.

        Parameters
        ----------
        maxPointDist: float, optional
            Maximum acceptable synchronization error, in seconds (default 2).
        minPointsNo: int, optional
            Minimum synchronization points no (default 20).
        outputCharEnc: str or None, optional
            Output character encoding, `None` for the same encoding as input
            subtitles (default 'UTF-8').
        windowSize: float, optional
            Synchronization window, in seconds. Timestamps will be corrected
            no more than this value (default 1800).
        minWordProb: float, optional
            Minimum speech recognition score, between 0 and 1 (default 0.3).
        jobsNo: int or None, optional
            Number of concurent synchronization threads, `None` for auto
            (default `None`).
        minWordLen: int, optional
            Minumum word length, in letters. Shorter words will not be used as
            synchronization points (default 5).
        minCorrelation: float, optional
            Minimum correlation factor, between 0 and 1 (default 0.9999).
        minWordsSim: float, optional
            Minimum words similarity to be used as synchronization points,
            between 0 and 1 (default 0.6).
        minEffort: float, optional
            Controls when synchronization should be stopped, between 0 and
            1 (default 0.5).
        outTimeOffset: float, optional
            Add constant offset to output subtitles, in seconds (default 0).
        overwrite: bool, optional
            Whether to overwrite existing output files. If not set, output file
            name will be suffixed with number if needed, to avoid overwritting
            (default `False`).
        """
        for key, val in kw.items():
            if key not in self._options:
                raise TypeError("Unexpected keyword argument '{}'".format(key))
            self._options[key] = val

    def synchronize(self, tasks, *, timeout=None, interactive=False):
        """Start task[s] synchronization.

        Parameters
        ----------
        tasks: SyncTask or iterable of SyncTask
            Single or several synchronization tasks.
        timeout: float or None, optional
            How often to call `onJobUpdate` callback, in seconds (if
            registered). `None` to not call it at all.
        interactive: bool, optional
            In interactive, tasks subtitles are not saved automatically
            (`minEffort` and task `out` field are ignored) and user is expected
            to save it manually either with `saveSynchronizedSubtitles` or
            `getSynchronizedSubtitles`.

        Notes
        -----
        Synchronization status changes are notified with callbacks registered
        in constructor.
        `onFinish` is called only when `tasks` is iterable (as oposed to single
        `SyncTask` object).
        """
        if self.isRunning():
            raise RuntimeError('Another synchronization in progress')

        logger.debug('synchronization options: %s', self._options)

        self._terminated = False
        if isinstance(tasks, Iterable):
            for task in tasks:
                self.validateTask(task, interactive=interactive)

            self._thread = threading.Thread(
                    target=self._run,
                    args=(tasks, timeout, interactive),
                    name='Synchronizer')
        else:
            self.validateTask(tasks, interactive=interactive)
            self._thread = threading.Thread(
                    target=self._runTask,
                    args=(tasks, timeout, interactive),
                    name='Synchronizer')
        self._thread.start()

    def terminate(self):
        """Terminate running synchronization.

        Does nothing if synchronization is not running.
        """
        if self.isRunning():
            self._terminated = True
            self._semaphore.release()

    def isRunning(self):
        """Check if synchronization is running.

        Returns
        -------
        bool
        """
        return self._thread and self._thread.is_alive()

    def wait(self):
        """Block until synchronization ends.

        Returns
        -------
        bool
            `True` if synchronization finished (either successfully or not),
            `False` if it was terminated with `SyncController.terminate`.
        """
        if self._thread:
            self._thread.join()
        return not self._terminated

    def getStatus(self):
        """Return current synchronization status.

        Returns
        -------
        SyncStatus or None
        """
        return self._sync and self._sync.getStatus()

    def getProgress(self):
        """Return synchronization progress.

        Returns
        -------
        float or None
            Progress of currently processed `SyncTask`, between 0 and 1.
            `None` if no task was run.
        """
        return self._sync and self._sync.getProgress()

    def getSynchronizedSubtitles(self):
        if self._sync is None:
            raise RuntimeError('Subtitles not synchronized')
        return self._sync.getSynchronizedSubtitles()

    def saveSynchronizedSubtitles(self, path=None, task=None):
        """Save synchronized subtitles.

        Parameters
        ----------
        path: str, optional
            Path to output subtitles.
        task: SyncTask, optional
            `out` field of task will be used as output description.

        Notes
        -----
        At least one parameter must be set. Subtitles will be saved in `path` or
        in `task`.out.path if `path` is not set. `task`.out character encoding
        and framerate will be used, if set.
        """
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

    def validateTask(self, task, *, interactive=False):
        """Check if task is properly defined.

        Parameters
        ----------
        task: SyncTask
            Task to validate.
        interactive: bool, optional
            For interactive synchronization `out` will not be vaildated.

        Raises
        ------
        Error
            Invalid task.
        KeyError or Exception
            Invalid `task`.out.path pattern.
        """
        sub, ref, out = task.sub, task.ref, task.out
        if sub is None or not sub.path or sub.no is None:
            raise Error('subtitles not set', task=task)
        if ref is None or not ref.path or ref.no is None:
            raise Error('reference file not set', task=task)
        if not interactive and (out is None or not out.path):
            raise Error('output path not set', task=task)
        if not interactive:
            out.validateOutputPattern()

    def _run(self, tasks, timeout, interactive):
        try:
            for no, task in enumerate(tasks):
                if not self._terminated:
                    logger.info('running task %i/%i: %r', no, len(tasks), task)
                    self._runTask(task, timeout, interactive)
                else:
                    break

        except Exception as err:
            logger.warning('%r', err, exc_info=True)
            self._onError(None, 'core', err)

        finally:
            logger.info('synchronization finished')
            self._onFinish(self._terminated)

    def _runTask(self, task, timeout, interactive):
        try:
            from .synchronizer import Synchronizer
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
                    and (interactive or minEffort >= 1.0 or status.effort < minEffort):
                self._semaphore.acquire(timeout=timeout)
                status = sync.getStatus()

                if timeout is not None:
                    now = time.monotonic()
                    if now - lastTime >= timeout:
                        lastTime = now
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

            if not interactive and succeeded and task.out:
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
