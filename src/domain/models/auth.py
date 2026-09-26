"""
Authentication and authorization data modeling.
"""

from dataclasses import dataclass
from enum import StrEnum


class Permission(StrEnum):
    """
    Set of permissions a user can have.

    - READ_CROPS: can read data from crops.
    - WRITE_CROPS: can write data from crops.
    - ARCHIVE_CROPS: can archive data from crops.
    - DELETE_CROPS: can delete data from crops.

    - READ_PLOTS: can read data from plots.
    - WRITE_PLOTS: can write data from plots.
    - ARCHIVE_PLOTS: can archive data from plots.
    - DELETE_PLOTS: can delete data from plots.

    - READ_SENSORS: can read data from sensors.
    - WRITE_SENSORS: can write data from sensors.
    - ARCHIVE_SENSORS: can archive data from sensors.
    - DELETE_SENSORS: can delete data from sensors.

    - PROVISION_DEVICES: can provision a device.
    - DECOMMISSION_DEVICES: can decommission a device.

    - READ_THRESHOLDS: can read data from thresholds.
    - WRITE_THRESHOLDS: can write data from thresholds.
    - ARCHIVE_THRESHOLDS: can archive data from thresholds.
    - DELETE_THRESHOLDS: can delete data from thresholds.

    - READ_ALL: can read all data.
    - WRITE_ALL: can write all data.
    - ARCHIVE_ALL: can archive all data.
    - DELETE_ALL: can delete all data.
    """

    READ_CROPS = 'crops:read'
    WRITE_CROPS = 'crops:write'
    ARCHIVE_CROPS = 'crops:archive'
    DELETE_CROPS = 'crops:delete'

    READ_PLOTS = 'plots:read'
    WRITE_PLOTS = 'plots:write'
    ARCHIVE_PLOTS = 'plots:archive'
    DELETE_PLOTS = 'plots:delete'

    READ_SENSORS = 'sensors:read'
    WRITE_SENSORS = 'sensors:write'
    ARCHIVE_SENSORS = 'sensors:archive'
    DELETE_SENSORS = 'sensors:delete'

    PROVISION_DEVICES = 'devices:provision'
    DECOMMISSION_DEVICES = 'devices:decommission'

    READ_THRESHOLDS = 'thresholds:read'
    WRITE_THRESHOLDS = 'thresholds:write'
    ARCHIVE_THRESHOLDS = 'thresholds:archive'
    DELETE_THRESHOLDS = 'thresholds:delete'

    READ_ALL = 'all:read'
    WRITE_ALL = 'all:write'
    ARCHIVE_ALL = 'all:archive'
    DELETE_ALL = 'all:delete'


PERMISSION_IMPLICATIONS: dict[Permission, set[Permission]] = {
    Permission.READ_ALL: {
        Permission.READ_CROPS,
        Permission.READ_PLOTS,
        Permission.READ_SENSORS,
        Permission.READ_THRESHOLDS,
    },
    Permission.WRITE_ALL: {
        Permission.WRITE_CROPS,
        Permission.WRITE_PLOTS,
        Permission.WRITE_SENSORS,
        Permission.WRITE_THRESHOLDS,
    },
    Permission.DELETE_ALL: {
        Permission.DELETE_CROPS,
        Permission.DELETE_PLOTS,
        Permission.DELETE_SENSORS,
        Permission.DELETE_THRESHOLDS,
    },
}


@dataclass(frozen=True)
class AuthenticatedUser:
    """
    Represents a user within the app with a set of permissions.

    :param id: Unique identifier for the user.
    :type id: str
    :param email: The email associated to the user.
    :type email: str
    :param permissions: Set of permissions the user has.
    :type permissions: set[:class:`Permission`]
    """

    id: str
    email: str
    permissions: set[Permission]

    def has_permission(self, permission: Permission) -> bool:
        """
        Check if user has a specific permission or a wildcard granting it.

        :param permission: The permission to check.
        :type permission: :class:`Permission`
        :return: True if the user has the permission, False otherwise.
        :rtype: bool
        """

        if permission in self.permissions:
            return True

        # Check if any granted permission implies this permission
        return any(
            permission in PERMISSION_IMPLICATIONS.get(granted, set())
            for granted in self.permissions
        )

    def has_any(self, *permissions: Permission) -> bool:
        """
        Returns True if the user satisfies at least one of the permissions.

        :param permissions: A list of permissions to check.
        :type permissions: list[:class:`Permission`]
        :return: True if the user has at least one of the permissions, False otherwise.
        :rtype: bool
        """

        return any(self.has_permission(p) for p in permissions)

    def has_all(self, *permissions: Permission) -> bool:
        """
        Returns True if the user satisfies all of the permissions.

        :param permissions: A list of permissions to check.
        :type permissions: list[:class:`Permission`]
        :return: True if the user has all of the permissions, False otherwise.
        :rtype: bool
        """

        return all(self.has_permission(p) for p in permissions)
