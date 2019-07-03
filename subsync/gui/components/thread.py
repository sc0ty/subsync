from functools import wraps
import wx


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
