"""Structured logging configuration for FastAPI."""

import logging
import sys
from typing import Any

import structlog
from structlog.typing import Processor

from .config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure structured logging based on settings."""

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_format == "json":
        processors: list[Processor] = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None, **initial_context: Any) -> structlog.stdlib.BoundLogger:
    """Get a logger instance with optional initial context."""
    logger = structlog.get_logger(name)
    if initial_context:
        logger = logger.bind(**initial_context)
    return logger
