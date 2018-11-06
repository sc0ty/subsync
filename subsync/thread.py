import wx
from functools import wraps
import threading

import logging
logger = logging.getLogger(__name__)


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


def gui_thread(func):
    '''Run in GUI thread
    If function is called from main GUI thread, it is called immediately.
    Otherwise it will be scheduled with wx.CallAfter
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if wx.IsMainThread():
            func(*args, **kwargs)
        else:
            wx.CallAfter(lambda args, kwargs: func(*args, **kwargs), args, kwargs)
    return wrapper


def gui_thread_cnt(counter_name):
    '''Run in GUI thread, count pending actions with counter_name
    Wraps object methods
    If function is called from main GUI thread, it is called immediately.
    Otherwise it will be scheduled with wx.CallAfter
    self.counter_name will count scheduled actions
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, counter_name):
                setattr(self, counter_name, AtomicInt())

            if wx.IsMainThread():
                func(self, *args, **kwargs)
            else:
                counter = getattr(self, counter_name)
                counter.up()
                wx.CallAfter(lambda self, args, kwargs, counter:
                        [ counter.down(), func(self, *args, **kwargs) ],
                        self, args, kwargs, counter)
        return wrapper
    return decorator

