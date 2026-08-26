"""
Authorization / Permission errors
"""

from domain.exceptions.base import DomainException


class PermissionDeniedException(DomainException):
    """User tried to perform an action to which they don't have permissions."""
