"""Custom exceptions for the library."""


class MyLibError(Exception):
    """Base exception for mylib."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """Initialize exception.

        Args:
            message: Error message
            code: Optional error code
        """
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(MyLibError):
    """Raised when input validation fails."""

    pass


class ConfigurationError(MyLibError):
    """Raised when configuration is invalid."""

    pass


class ProcessingError(MyLibError):
    """Raised when processing fails."""

    pass
