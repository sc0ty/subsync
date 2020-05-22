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
                self.blocker = wx.PowerResource()
                reason = 'subsync: synchronization in progress'
                if self.blocker.Acquire(wx.POWER_RESOURCE_SYSTEM, reason):
                    logger.info('acquired system suspend lock')
                else:
                    logger.warning('couldn\'t acquire system suspend lock')
                    self.blocker = None
            except Exception as e:
                logger.warning('acquire system suspend lock failed: %r', e, exc_info=True)
                self.blocker = None
        else:
            logger.warning('suspend locking not available for your installation')

    def unlock(self):
        if self.blocker:
            logger.info('releasing system suspend lock')
            try:
                self.blocker.Release(wx.POWER_RESOURCE_SYSTEM)
            except Exception as e:
                logger.warning('release system suspend lock failed: %r', e, exc_info=True)
            self.blocker = None

