"""
Application-wide logging configuration.

Called once at startup (see app/main.py). Every module in the app should
retrieve its own logger via `logging.getLogger(__name__)` rather than
printing to stdout - this keeps log output structured and filterable.
"""
import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
