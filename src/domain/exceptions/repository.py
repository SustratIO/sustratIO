"""
Persistence / Data access errors.
"""

from domain.exceptions.base import DomainException


class EntityNotFoundException(DomainException):
    """User tried to retrieve data that doesn't exist."""


class EntityAlreadyExistsException(DomainException):
    """Raised on unique constraint conflicts (e.g., duplicate slug or name)."""


class RepositoryDataAccessException(DomainException):
    """Generic fallback exception for unexpected DB connectivity or I/O failures."""
