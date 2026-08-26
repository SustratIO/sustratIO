"""
Authentication errors on the adapters.
"""

from domain.exceptions.repository import DomainException


class JWTAuthenticationError(DomainException):
    """Raised when failed to authenticate a user using a JWT token."""
