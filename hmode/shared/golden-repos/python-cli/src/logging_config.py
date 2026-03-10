"""Logging configuration using structlog."""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from .config import Settings


def configure_logging(settings: Settings, verbose: bool = False) -> None:
    """Configure structured logging."""
    log_level = "DEBUG" if verbose else settings.log_level.upper()

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, log_level),
    )

    # Shared processors
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.log_format == "json":
        # JSON format for production
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, log_level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Console format for development
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, log_level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str, **initial_values: Any) -> structlog.stdlib.BoundLogger:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name, **initial_values)
