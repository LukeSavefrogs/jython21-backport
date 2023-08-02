""" Polyfill for the `logging` module.

WARNING: 
    This module is not complete by any means, nor it follows strictly the `logging` module API.

    For example, here are some differences:
    - The `Logger` class does not currently support parents
    - The `Logger` class does not currently support filters
    - The `Logger` class does not currently support handlers
    - The `Logger` class does not currently support propagation
"""
import sys as _sys
import time as _time

import unittest as _unittest

try:
    # fmt: off
    from java.lang.management import ManagementFactory as _ManagementFactory # pyright: ignore[reportMissingImports]
    # fmt: on
except ImportError:
    pass

try:
    import warnings
except ImportError:
    pass

__all__ = ["getLogger", "basicConfig"]

# --------------------- Transform levels to values and viceversa ---------------------
#                  (completely stripped from the `logging` module :D)
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOTSET",
}
_nameToLevel = {
    "CRITICAL": CRITICAL,
    "FATAL": FATAL,
    "ERROR": ERROR,
    "WARN": WARNING,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}


def _checkLevel(level):
    # type: (str|int) -> int
    """Given a level name or level number, return the level number.

    Args:
        level (str|int): The level name or number.

    Returns:
        int: The level number.
    """
    if type(level).__name__ in ["int", "org.python.core.PyInteger"]:
        rv = level
    elif str(level) == level:
        if level not in _nameToLevel.keys():
            raise ValueError("Unknown level: %r" % level)
        rv = _nameToLevel[level]
    else:
        raise TypeError("Level not an integer or a valid string: %r" % level)
    return rv


def getLevelName(level):
    """
    Return the textual or numeric representation of logging level 'level'.

    If the level is one of the predefined levels (CRITICAL, ERROR, WARNING,
    INFO, DEBUG) then you get the corresponding string. If you have
    associated levels with names using addLevelName then the name you have
    associated with 'level' is returned.

    If a numeric value corresponding to one of the defined levels is passed
    in, the corresponding string representation is returned.

    If a string representation of the level is passed in, the corresponding
    numeric value is returned.

    If no matching numeric or string value is passed in, the string
    'Level %s' % level is returned.
    """
    # See Issues #22386, #27937 and #29220 for why it's this way
    result = _levelToName.get(level)
    if result is not None:
        return result

    result = _nameToLevel.get(level)
    if result is not None:
        return result
    return "Level %s" % level


# ------------------------------------------------------------------------------------

ROOT_LOGGER_NAME = "root"
DEFAULT_LOGGING_FORMAT = "%(levelname)s:%(name)s:%(message)s"
DEFAULT_LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M %Z"


# Define a logger class useful for printing helpful messages
class Logger:
    """Logger class for Python 2.x that mimics the `logging` module."""

    def __init__(
        self,
        name,
        level=NOTSET,
    ):
        """Create the logger.

        Args:
            name (str, optional): The name of the logger.
            level (str, optional): The minimum logging level. Defaults to "info".
        """
        self.name = name

        self.level = _checkLevel(level)
        self._format = DEFAULT_LOGGING_FORMAT
        self._time_format = DEFAULT_LOGGING_DATE_FORMAT

        # From the `logging` module
        self._cache = {}
        self.parent = None

        try:
            self._process_id = (
                _ManagementFactory.getRuntimeMXBean().getName().split("@")[0]
            )
        except:
            self._process_id = 0

    def setLevel(self, level):
        # type: (str) -> None
        """Sets the minimum level of the current logger."""
        self.level = _checkLevel(level)
        self._cache = {}

    def getEffectiveLevel(self):
        """
        Get the effective level for this logger.

        Loop through this logger and its parents in the logger hierarchy,
        looking for a non-zero logging level. Return the first one found.
        """
        logger = self
        while logger:
            if logger.level:
                return logger.level
            logger = logger.parent
        return NOTSET

    def isEnabledFor(self, level):
        """
        Is this logger enabled for level 'level'?
        """
        try:
            return self._cache[level]
        except KeyError:
            is_enabled = level >= self.getEffectiveLevel()
            self._cache[level] = is_enabled
            return is_enabled

    def log(self, _log_level, message):
        # type: (str, str|int) -> None
        """Base function used by the other logging methods to abstract the logic.

        Args:
            message (str): The message to log.
            _log_level (str|int): The level of the message.
        """
        if not self.isEnabledFor(_log_level):
            return

        creation_time = _time.time()

        caller = _sys._getframe().f_back.f_back.f_code.co_name
        if caller == "?":
            caller = "__main__"

        # See https://docs.python.org/3/library/logging.html#logrecord-attributes
        # fmt: off
        print(
            self._format
            % {
                "asctime": _time.strftime(
                    self._time_format, _time.localtime(creation_time)
                ),
                "created": creation_time,
                "filename": "__NOT_IMPLEMENTED__",         # TODO: LogRecord 'filename' not implemented
                "funcName": caller,
                "levelname": getLevelName(_log_level),
                "levelno": _log_level,
                "lineno": 0,                               # TODO: LogRecord 'lineno' not implemented
                "message": str(message),
                "module": "__NOT_IMPLEMENTED__",           # TODO: LogRecord 'module' not implemented
                "msecs": int(str("%.3f" % creation_time).split(".")[1]),
                "name": self.name,
                "pathname": "__NOT_IMPLEMENTED__",         # TODO: LogRecord 'pathname' not implemented
                "process": int(self._process_id),
                "processName": "__NOT_IMPLEMENTED__",      # TODO: LogRecord 'processName' not implemented
                "relativeCreated": 0,                      # TODO: LogRecord 'relativeCreated' not implemented
                "thread": 0,                               # TODO: LogRecord 'thread' not implemented
                "threadName": "__NOT_IMPLEMENTED__",       # TODO: LogRecord 'threadName' not implemented
            }
        )
        # fmt: on

    def debug(self, message=""):
        self.log(DEBUG, message)

    def info(self, message=""):
        self.log(INFO, message)

    def warning(self, message=""):
        self.log(WARNING, message)

    def error(self, message=""):
        self.log(ERROR, message)

    def critical(self, message=""):
        self.log(CRITICAL, message)

    def fatal(self, message=""):
        self.log(FATAL, message)


class RootLogger(Logger):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """

    def __init__(self, level):
        """
        Initialize the logger with the name "root".
        """
        Logger.__init__(self, ROOT_LOGGER_NAME, level)


root = RootLogger(WARNING)


def getLogger(name=None):
    # type: (str) -> Logger
    """Returns a logger object with the specified name."""
    if name is None or (type(name).__class__ in ["str", "org.python.core.PyString"] and name == ROOT_LOGGER_NAME):
        return root

    return Logger(name)


def basicConfig(**kwargs):
    """Basic configuration for the logging system.

    Args:
        level (str, optional): The minimum logging level. Defaults to "info".
        format (str, optional): The logging format as specified in the docs (https://docs.python.org/3/library/logging.html#logrecord-attributes). Defaults to `%(levelname)s:%(name)s:%(message)s`.
        datefmt (str, optional): The human readable time format. Defaults to `%Y-%m-%d %H:%M %Z`.

    Raises:
        ValueError: If an unrecognised argument is passed.

    Examples:
        ```pycon
        >>> import polyfills.logging as logging
        >>> logging.basicConfig(level="DEBUG")
        >>> logging.info("Hello World!")
        INFO:root:Hello World!
        >>> logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M")
        >>> logging.info("Hello World!")
        [2021-03-21 16:20] INFO - root - Hello World!
        ```
    """
    unrecognised_keys = [
        key for key in kwargs.keys() if key not in ["level", "format", "datefmt"]
    ]
    if unrecognised_keys:
        raise ValueError(
            "Unrecognised argument(s): %s" % (", ".join(unrecognised_keys))
        )

    logger_level = kwargs.get("level", None)
    logger_format = kwargs.get("format", None)
    logger_datefmt = kwargs.get("datefmt", None)

    if logger_level is not None:
        root.setLevel(logger_level)

    if logger_format is not None:
        root._format = logger_format

    if logger_datefmt is not None:
        root._time_format = logger_datefmt


# ---------------------------------------------------------------------------
# Utility functions at module level.
# Basically delegate everything to the root logger.
# ---------------------------------------------------------------------------


def critical(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger. If the logger
    has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.critical(msg, *args, **kwargs)


fatal = critical


def error(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.error(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger, with exception
    information. If the logger has no handlers, basicConfig() is called to add
    a console handler with a pre-defined format.
    """
    error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """
    Log a message with severity 'WARNING' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.warning(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    try:
        warnings.warn(
            "The 'warn' function is deprecated, " "use 'warning' instead",
            DeprecationWarning,
            2,
        )
    except NameError:
        pass
    warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """
    Log 'msg % args' with the integer severity 'level' on the root logger. If
    the logger has no handlers, call basicConfig() to add a console handler
    with a pre-defined format.
    """
    # if len(root.handlers) == 0:
    #     basicConfig()
    root.log(level, msg, *args, **kwargs)


class LoggingTestCase(_unittest.TestCase):
    def test_getLogger_name(self):
        logger = getLogger()
        self.assertEqual(logger.name, ROOT_LOGGER_NAME)

        logger = getLogger("test_logger")
        self.assertEqual(logger.name, "test_logger")

    def test_setlevel(self):
        _true = 1 == 1
        _false = 1 == 0

        logger = getLogger()
        self.assertEqual(logger.getEffectiveLevel(), WARNING)
        self.assertEqual(logger.isEnabledFor(WARNING), _true)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

        logger = getLogger("test_logger")
        self.assertEqual(logger.getEffectiveLevel(), NOTSET)
        self.assertEqual(logger.isEnabledFor(WARNING), _true)
        self.assertEqual(logger.isEnabledFor(DEBUG), _true)

        logger.setLevel("DEBUG")
        self.assertEqual(logger.getEffectiveLevel(), DEBUG)
        self.assertEqual(logger.isEnabledFor(WARNING), _true)
        self.assertEqual(logger.isEnabledFor(DEBUG), _true)

        logger.setLevel("INFO")
        self.assertEqual(logger.getEffectiveLevel(), INFO)
        self.assertEqual(logger.isEnabledFor(WARNING), _true)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

        logger.setLevel("WARNING")
        self.assertEqual(logger.getEffectiveLevel(), WARNING)
        self.assertEqual(logger.isEnabledFor(WARNING), _true)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

        logger.setLevel("ERROR")
        self.assertEqual(logger.getEffectiveLevel(), ERROR)
        self.assertEqual(logger.isEnabledFor(FATAL), _true)
        self.assertEqual(logger.isEnabledFor(WARNING), _false)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

        logger.setLevel("CRITICAL")
        self.assertEqual(logger.getEffectiveLevel(), CRITICAL)
        self.assertEqual(logger.isEnabledFor(FATAL), _true)
        self.assertEqual(logger.isEnabledFor(WARNING), _false)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

        logger.setLevel("FATAL")
        self.assertEqual(logger.getEffectiveLevel(), FATAL)
        self.assertEqual(logger.isEnabledFor(FATAL), _true)
        self.assertEqual(logger.isEnabledFor(WARNING), _false)
        self.assertEqual(logger.isEnabledFor(DEBUG), _false)

    def test_logger_singleton(self):
        logger = getLogger()
        self.assertEqual(logger, root)

        logger = getLogger("test_logger")
        self.assertNotEqual(logger, root)

        # BUG: Multiple calls to getLogger with the same name should return the same logger object
        # self.assertEqual(getLogger("logger"), getLogger("logger"))


if __name__ == "__main__":
    print("--------------- Testing root logger ---------------")
    basicConfig(format="%(levelname)s: %(message)s")
    info("This is a message with severity 'INFO'")
    debug("This is a message with severity 'DEBUG'")
    warning("This is a message with severity 'WARNING'")
    error("This is a message with severity 'ERROR'")
    critical("This is a message with severity 'CRITICAL'")
    fatal("This is a message with severity 'FATAL'")
    log(CRITICAL, "This is a custom log with severity 'CRITICAL'")

    assert getLogger() == getLogger(name=None)

    print("\n\n")
    print("--------------- Testing custom logger ---------------")
    logger = getLogger("test_logger")
    print(
        "Effective level for logger '%s': %d\n"
        % (logger.name, logger.getEffectiveLevel())
    )

    for method in ["debug", "info", "warning", "error", "critical", "fatal"]:
        getattr(logger, method)("This is a message with level '%s'" % method.upper())

    print("\n\n")
    print("--------------- Setting level to 'WARNING' ---------------")

    logger.setLevel("WARNING")
    print(
        "Effective level for logger '%s': %d\n"
        % (logger.name, logger.getEffectiveLevel())
    )
    for method in ["debug", "info", "warning", "error", "critical", "fatal"]:
        getattr(logger, method)("This is a message with level '%s'" % method.upper())
