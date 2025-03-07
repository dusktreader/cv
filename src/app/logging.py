import inspect
import logging
import sys

from loguru import logger


def init_logs(verbose=False):
    logger.remove()

    if verbose:
        logger.add(sys.stdout, level="DEBUG")

    logger.debug("Logging initialized")


def hijack_weasyprint():
    logging.basicConfig(handlers=[InterceptHandler()], level=0)


class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
