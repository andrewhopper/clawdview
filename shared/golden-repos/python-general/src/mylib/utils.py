"""Utility functions for the library."""

import re
from typing import Any, TypeVar

from pydantic import ValidationError

T = TypeVar("T")


def validate_input(
    data: dict[str, Any],
    required_keys: list[str],
    optional_keys: list[str] | None = None,
) -> tuple[bool, str | None]:
    """Validate input data has required keys.

    Args:
        data: Input dictionary to validate
        required_keys: Keys that must be present
        optional_keys: Keys that are allowed but not required

    Returns:
        Tuple of (is_valid, error_message)
    """
    missing = [key for key in required_keys if key not in data]
    if missing:
        return False, f"Missing required keys: {', '.join(missing)}"

    if optional_keys is not None:
        allowed = set(required_keys) | set(optional_keys)
        extra = [key for key in data if key not in allowed]
        if extra:
            return False, f"Unknown keys: {', '.join(extra)}"

    return True, None


def format_output(
    data: Any,
    format_type: str = "default",
    indent: int = 2,
) -> str:
    """Format data for output.

    Args:
        data: Data to format
        format_type: Output format (default, compact, pretty)
        indent: Indentation for pretty format

    Returns:
        Formatted string representation
    """
    import json

    if format_type == "compact":
        return json.dumps(data, separators=(",", ":"), default=str)
    elif format_type == "pretty":
        return json.dumps(data, indent=indent, default=str)
    else:
        return json.dumps(data, default=str)


def slugify(text: str, separator: str = "-") -> str:
    """Convert text to URL-safe slug.

    Args:
        text: Text to convert
        separator: Character to use as separator

    Returns:
        Slugified text
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", separator, text)
    return text.strip(separator)


def chunk_list(items: list[T], chunk_size: int) -> list[list[T]]:
    """Split a list into chunks.

    Args:
        items: List to split
        chunk_size: Maximum items per chunk

    Returns:
        List of chunks
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
