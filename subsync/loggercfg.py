import logging
import gizmo


class BlacklistFilter(logging.Filter):
    def __init__(self, names):
        self.blacklist = set(names)

    def filter(self, record):
        return record.name not in self.blacklist


_activeFilter = None


def init(level=None, path=None):
    logging.basicConfig(
            format='%(asctime)s:%(threadName)12.12s:%(levelname)8.8s:%(name)24.24s: %(message)s',
            level=level,
            filename=path)

    def print_log(level, m, msg):
        logging.getLogger(m).log(level, msg.strip().replace('\n', '; '))

    gizmo.setLoggerCallback(print_log)
    gizmo.setDebugLevel(level)


def terminate():
    gizmo.setLoggerCallback(None)


def setLevel(level):
    logger = logging.getLogger()
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
    gizmo.setDebugLevel(level)


def setBlacklistFilters(filters):
    global _activeFilter

    if _activeFilter:
        for handler in logging.root.handlers:
            handler.removeFilter(_activeFilter)

        _activeFilter = None

    if filters:
        _activeFilter = BlacklistFilter(filters)

        for handler in logging.root.handlers:
            handler.addFilter(_activeFilter)

