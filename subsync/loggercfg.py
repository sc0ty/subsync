import logging
import threading
import sys
import gizmo


class BlacklistFilter(logging.Filter):
    def __init__(self, names):
        super().__init__()
        self.blacklist = set(names)

    def filter(self, record):
        if record.name in self.blacklist:
            return False

        try:
            pos = -1
            while True:
                pos = record.name.index('.', pos+1)
                if record.name[:pos] in self.blacklist:
                    return False
        except:
            return True


initialized = False
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

    def excepthook(type, exc, tb):
        logging.getLogger('RUNTIME').critical("Unhandled exception", exc_info=(type, exc, tb))
        sys.__excepthook__(type, exc, tb)

    sys.excepthook = excepthook
    setup_thread_excepthook()

    def print_log(level, m, msg):
        logging.getLogger(m).log(level, msg.strip().replace('\n', '; '))

    gizmo.setLoggerCallback(print_log)
    gizmo.setDebugLevel(numLevel)

    global initialized
    initialized = True


def setup_thread_excepthook():
    # monkey patching threading.Thread to also call sys.excepthook
    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):
        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            try:
                run_original(*args2, **kwargs2)
            except Exception:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_except_hook
    threading.Thread.__init__ = init


def terminate():
    if initialized:
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

