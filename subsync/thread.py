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
        self.loop = None
        self.task = None
        self.thread = None
        self.name = name
        self.job = job

    def start(self, *args, **kwargs):
        thread = threading.Thread(
                name=self.name,
                args=[self.job] + list(args),
                kwargs=kwargs,
                target=self._run)

        thread.start()
        self.thread = thread

    def startSynchronous(self, *args, **kwargs):
        self._run(self.job, *args, **kwargs)

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.task.cancel)
        if self.thread and self.thread.isAlive():
            self.thread.join()

    def isRunning(self):
        return self.thread and self.thread.isAlive()

    def getResult(self):
        if self.task:
            try:
                return self.task.result()
            except CancelledError or InvalidStateError:
                pass

    def _run(self, job, *args, **kwargs):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.task = asyncio.ensure_future(job(*args, **kwargs))
        self.loop.run_until_complete(self.task)
