"""Python library template - a gold standard example."""

from .core import MyClass
from .utils import format_output, validate_input
from .logging import get_logger, configure_logging
from .config import get_config, configure, LibraryConfig

__version__ = "0.1.0"
__all__ = [
    "MyClass",
    "format_output",
    "validate_input",
    "get_logger",
    "configure_logging",
    "get_config",
    "configure",
    "LibraryConfig",
]
