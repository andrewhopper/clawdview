"""Tests for utils module."""

import pytest

from mylib.utils import validate_input, format_output, slugify, chunk_list


class TestValidateInput:
    """Tests for validate_input function."""

    def test_valid_input(self) -> None:
        """Test validation passes with required keys."""
        is_valid, error = validate_input(
            {"name": "test", "value": 123},
            required_keys=["name", "value"],
        )
        assert is_valid is True
        assert error is None

    def test_missing_required_key(self) -> None:
        """Test validation fails with missing key."""
        is_valid, error = validate_input(
            {"name": "test"},
            required_keys=["name", "value"],
        )
        assert is_valid is False
        assert "value" in error

    def test_unknown_key_with_optional(self) -> None:
        """Test validation fails with unknown key."""
        is_valid, error = validate_input(
            {"name": "test", "extra": "value"},
            required_keys=["name"],
            optional_keys=[],
        )
        assert is_valid is False
        assert "extra" in error


class TestFormatOutput:
    """Tests for format_output function."""

    def test_default_format(self) -> None:
        """Test default format."""
        result = format_output({"key": "value"})
        assert '"key"' in result
        assert '"value"' in result

    def test_compact_format(self) -> None:
        """Test compact format."""
        result = format_output({"key": "value"}, format_type="compact")
        assert " " not in result

    def test_pretty_format(self) -> None:
        """Test pretty format."""
        result = format_output({"key": "value"}, format_type="pretty")
        assert "\n" in result


class TestSlugify:
    """Tests for slugify function."""

    def test_basic_slugify(self) -> None:
        """Test basic slug creation."""
        assert slugify("Hello World") == "hello-world"

    def test_special_characters(self) -> None:
        """Test removal of special characters."""
        assert slugify("Hello! World?") == "hello-world"

    def test_custom_separator(self) -> None:
        """Test custom separator."""
        assert slugify("Hello World", separator="_") == "hello_world"


class TestChunkList:
    """Tests for chunk_list function."""

    def test_even_chunks(self) -> None:
        """Test even chunking."""
        result = chunk_list([1, 2, 3, 4], 2)
        assert result == [[1, 2], [3, 4]]

    def test_uneven_chunks(self) -> None:
        """Test uneven chunking."""
        result = chunk_list([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]
