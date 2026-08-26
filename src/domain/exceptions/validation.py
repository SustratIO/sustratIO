"""
Model & DTO validation errors
"""

from domain.exceptions.base import DomainException


class ValidationError(DomainException):
    """Data validation exceptions."""


class StringTooLongError(ValidationError):
    """Raised when a string field exceeds maximum length constraints."""

    def __init__(self, field_name: str, max_length: int, current_length: int):
        super().__init__(
            f"Field '{field_name}' exceeded maximum allowed characters "
            f'({max_length}). Current: {current_length}'
        )
