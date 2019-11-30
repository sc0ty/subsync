import logging
import gizmo


class BlacklistFilter(logging.Filter):
    def __init__(self, names):
        super().__init__()
        self.blacklist = set(names)

    def filter(self, record):
        return record.name not in self.blacklist


_activeFilter = None


def init(level=None, path=None):
    logging.captureWarnings(True)
    numLevel = parseLevel(level)

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
            format='%(asctime)s.%(msecs)03i: %(threadName)12.12s: %(levelname)8.8s: %(name)26s: %(message)s',
            datefmt='%H:%M:%S',
            level=numLevel,
            filename=path)

    def print_log(level, m, msg):
        logging.getLogger(m).log(level, msg.strip().replace('\n', '; '))

    gizmo.setLoggerCallback(print_log)
    gizmo.setDebugLevel(numLevel)


def terminate():
    gizmo.setLoggerCallback(None)


def setLevel(level):
    numLevel = parseLevel(level)
    logger = logging.getLogger()
    logger.setLevel(numLevel)
    for handler in logger.handlers:
        handler.setLevel(numLevel)
    gizmo.setDebugLevel(numLevel)


def parseLevel(level):
    try:
        return int(level)
    except:
        try:
            return getattr(logging, level)
        except:
            return logging.WARNING


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

