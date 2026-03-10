"""Tests for core module."""

from mylib import MyClass
from mylib.core import Result, BaseEntity


class TestResult:
    """Tests for Result class."""

    def test_ok_result(self) -> None:
        """Test creating successful result."""
        result = Result.ok({"key": "value"}, extra="data")
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error is None
        assert result.metadata["extra"] == "data"

    def test_fail_result(self) -> None:
        """Test creating failed result."""
        result = Result.fail("Something went wrong")
        assert result.success is False
        assert result.data is None
        assert result.error == "Something went wrong"


class TestMyClass:
    """Tests for MyClass."""

    def test_initialization(self) -> None:
        """Test class initialization."""
        instance = MyClass(name="test")
        assert instance.name == "test"
        assert instance.config == {}

    def test_initialization_with_config(self) -> None:
        """Test initialization with config."""
        instance = MyClass(name="test", config={"key": "value"})
        assert instance.config["key"] == "value"

    def test_process_success(self, my_instance: MyClass) -> None:
        """Test successful processing."""
        result = my_instance.process({"input": "data"})
        assert result.success is True
        assert result.data is not None
        assert result.data["processor"] == "test"

    def test_configure(self, my_instance: MyClass) -> None:
        """Test configuration update."""
        my_instance.configure(new_key="new_value")
        assert my_instance.config["new_key"] == "new_value"
