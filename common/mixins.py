import logging
import sys
import os


class LoggerMixin:
    """Provides a logger that outputs to stdout using the class name as the logger name."""

    def __init__(self):
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
            logger = logging.getLogger(logger_name)

            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(
                    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)

                log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
                logger.setLevel(log_level)
                logger.propagate = False

            self._logger = logger

        return self._logger
