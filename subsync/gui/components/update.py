from functools import wraps
from contextlib import contextmanager


@contextmanager
def updateLocker(obj):
    try:
        obj.Freeze()
        yield
    finally:
        obj.Thaw()


def update_lock(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            self.Freeze()
            res = method(self, *args, **kwargs)
        finally:
            self.Thaw()
        return res
    return wrapper
