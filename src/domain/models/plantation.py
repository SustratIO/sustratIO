from dataclasses import dataclass

from domain.models.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifierMixin,
)


@dataclass(kw_only=True)
class Plantation(UniqueIdentifierMixin, AuditTimestampMixin):
    """
    Plantation is a data class that represents a plantation in the system.

    :param name: The name of the plantation.
    :type name: str
    :param owner_id: The ID of the owner of the plantation.
    :type owner_id: str
    """

    name: str
    owner_id: str
