"""
Model & DTO validation errors
"""

from domain.exceptions.base import DomainException


class ValidationError(DomainException):
    """Data validation exceptions."""


class InvalidCursorDataError(ValidationError):
    """Raised when a cursor cannot be decoded or has an invalid format."""

    def __init__(
        self,
        message: str = 'The provided cursor is invalid or malformed.',
    ):
        super().__init__(message)


class StringTooLongError(ValidationError):
    """Raised when a string field exceeds maximum length constraints."""

    def __init__(self, field_name: str, max_length: int, current_length: int):
        super().__init__(
            f"Field '{field_name}' exceeded maximum allowed characters "
            f'({max_length}). Current: {current_length}'
        )


class TimestampWithoutTimezoneError(ValidationError):
    """Raised when a timestamp is created without timezone."""

    def __init__(self, field_name: str):
        super().__init__(f"Field '{field_name}' doesn't have timezone.")
