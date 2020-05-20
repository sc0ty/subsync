import wx

import logging
logger = logging.getLogger(__name__)


class SuspendBlocker(object):
    def __init__(self):
        self.blocker = None

    def hasLock():
        return hasattr(wx, 'PowerResource')

    def lock(self):
        if SuspendBlocker.hasLock():
            try:
                self.lock = wx.PowerResource()
                reason = 'subsync: synchronization in progress'
                if self.lock.Acquire(wx.POWER_RESOURCE_SYSTEM, reason):
                    logger.info('acquired system suspend lock')
                else:
                    logger.warning('couldn\'t acquire system suspend lock')
                    self.lock = None
            except Exception as e:
                logger.warning('acquire system suspend lock failed: %r', e, exc_info=True)
                self.lock = None
        else:
            logger.warning('suspend locking not available for your installation')

    def unlock(self):
        if self.lock:
            logger.info('releasing system suspend lock')
            try:
                self.lock.Release(wx.POWER_RESOURCE_SYSTEM)
            except Exception as e:
                logger.warning('release system suspend lock failed: %r', e, exc_info=True)
            self.lock = None

