"""
Authentication and authorization data modeling.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import uuid


class Permission(StrEnum):
    """
    Set of permissions a user can have.

    - READ_CROP: can read data from crop.
    - READ_SENSOR: can read data from sensor.
    - WRITE_CROP: can write data from crop.
    - WRITE_SENSOR: can write data from sensor.
    - DELETE_CROP: can delete data from crop.
    - DELETE_SENSOR: can delete data from sensor.
    """

    READ_CROP = 'read:crop'
    READ_SENSOR = 'read:sensor'
    WRITE_CROP = 'write:crop'
    WRITE_SENSOR = 'write:sensor'
    DELETE_CROP = 'delete:crop'
    DELETE_SENSOR = 'delete:sensor'


@dataclass(frozen=True)
class AuthenticatedUser:
    """
    Represents a user within the app with a set of permissions.

    :param id: Unique identifier for the user.
    :type id: :class:`uuid.UUID`
    :param email: The email associated to the user.
    :type email: str
    :param role: The role for the user.
    :type role: str
    """

    id: uuid.UUID
    email: str
    permissions: set[Permission]
