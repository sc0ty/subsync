import threading
import asyncio


class AtomicValue(object):
    def __init__(self, value=None):
        self.value = value
        self.lock = threading.Lock()

    def set(self, value):
        with self.lock:
            self.value = value

    def get(self):
        with self.lock:
            return self.value

    def swap(self, newValue):
        with self.lock:
            value = self.value
            self.value = newValue
        return value


class AtomicInt(AtomicValue):
    def __init__(self, value=0):
        super().__init__(value)

    def up(self, num=1):
        with self.lock:
            self.value += num

    def down(self, num=1):
        with self.lock:
            self.value -= num


class AsyncJob(object):
    def __init__(self, job, name=None):
        self._loop = None
        self._task = None
        self._thread = None
        self._name = name
        self._job = job

    def start(self, *args, **kwargs):
        thread = threading.Thread(
                name=self._name,
                args=[self._job] + list(args),
                kwargs=kwargs,
                target=self._run)

        thread.start()
        self._thread = thread

    def startSynchronous(self, *args, **kwargs):
        self._run(self._job, *args, **kwargs)

    def stop(self):
        if self._loop:
            self._loop.call_soon_threadsafe(self._task.cancel)
        if self._thread and self._thread.isAlive():
            self._thread.join()

    def isRunning(self):
        return self._thread and self._thread.isAlive()

    def getResult(self):
        if self._task:
            try:
                return self._task.result()
            except asyncio.CancelledError or asyncio.InvalidStateError:
                pass

    def _run(self, job, *args, **kwargs):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._task = asyncio.ensure_future(job(*args, **kwargs))
        try:
            self._loop.run_until_complete(self._task)
        except asyncio.CancelledError:
            pass
