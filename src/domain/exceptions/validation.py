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


class OutOfBoundsError(ValidationError):
    """Raised when a coordinate is out of valid geographical bounds."""

    def __init__(self, field_name: str, value: str):
        """
        Initialize the OutOfBoundsError.

        :param field_name: The name of the field that has an out-of-bounds
                           value.
        :type field_name: str
        :param value: String representation of the out-of-bounds value so it
                      can support Decimal and other types.
        :type value: str
        """

        super().__init__(
            f"Field '{field_name}' has an out-of-bounds value: {value}."
        )
