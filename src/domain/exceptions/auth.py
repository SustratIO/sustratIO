"""
Authorization / Permission errors
"""

from domain.exceptions.base import DomainException


class JWTAuthenticationError(DomainException):
    """Raised when failed to authenticate a user using a JWT token."""


class PermissionDeniedException(DomainException):
    """User tried to perform an action to which they don't have permissions."""
