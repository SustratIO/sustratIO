"""
The models contained here hold and perform transformations on data regarding
common and specific crops.
"""

import datetime
from dataclasses import dataclass

from domain.exceptions.validation import StringTooLongError
from domain.models.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifier,
)


@dataclass(kw_only=True)
class Crop(UniqueIdentifier, AuditTimestampMixin):
    """
    :param name: Common crop name.
    :type name: str
    :param species: Botanical species name.
    :type species: str | None
    :param description: Description of the crop.
    :type description: str | None
    :param notes: Notes associated to this crop.
    :type notes: str | None
    :param planted_at: Timestamp when planted.
    :type planted_at: :class:`datetime.datetime`
    :param owner_id: The user this crops belongs to.
    :type owner_id: str
    """

    name: str
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    planted_at: datetime.datetime
    owner_id: str

    def __post_init__(self):
        if len(self.name) > 50:
            raise StringTooLongError(
                field_name='name',
                max_length=50,
                current_length=len(self.name),
            )


@dataclass(kw_only=True)
class CropSearchCriteria:
    """
    Filter parameters for querying :class:`Crop` entities.

    :param name: Common crop name.
    :type name: str | None
    :param species: Botanical species name.
    :type species: str | None
    :param description: Description of the crop.
    :type description: str | None
    :param notes: Notes associated to this crop.
    :type notes: str | None
    :param planted_at: Timestamp when planted.
    :type planted_at: :class:`datetime.datetime` | None
    :param owner_id: The user this crops belongs to.
    :type owner_id: str | None
    """

    name: str | None = None
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    planted_at: datetime.datetime | None = None
    owner_id: str | None = None
