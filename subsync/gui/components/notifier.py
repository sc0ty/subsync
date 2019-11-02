import wx


class SignalNotifier(object):
    def __init__(self, *listeners):
        self.disabledCnt = 0
        self.queuedCnt = 0
        self.listeners = listeners or []

    def addListener(self, listener):
        self.listeners.append(listener)

    def removeListener(self, listener):
        self.listeners.remove(listener)

    def enable(self, enabled=True):
        if enabled:
            self.disabledCnt -= 1
            if self.disabledCnt == 0 and self.queuedCnt:
                self.emit()
        else:
            self.disable()

    def disable(self):
        self.disabledCnt += 1

    def clear(self):
        self.queuedCnt = 0

    def emit(self):
        self.queuedCnt += 1
        if self.disabledCnt == 0:
            self.notifyListeners()

    def notifyListeners(self):
        self.queuedCnt = 0
        for listener in self.listeners:
            listener()


class DelayedSignalNotifier(SignalNotifier):
    def __init__(self, delay=0.02, *listeners):
        super().__init__(*listeners)
        self.delay = int(delay * 1000)
        self.timer = None

    def disable(self):
        super().disable()
        if self.timer:
            self.timer.Stop()
            self.timer = None

    def clear(self):
        super().clear()
        if self.timer:
            self.timer.Stop()
            self.timer = None

    def emit(self):
        self.queuedCnt += 1
        if self.disabledCnt == 0:
            if self.timer:
                self.timer.Stop()
            self.timer = wx.CallLater(self.delay, self.notifyListeners)
