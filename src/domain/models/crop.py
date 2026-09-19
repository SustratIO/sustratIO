"""
The models contained here hold and perform transformations on data regarding
common and specific crops.
"""

import datetime
from dataclasses import dataclass

from domain.exceptions.validation import (
    StringTooLongError,
    TimestampWithoutTimezoneError,
)
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
        max_name_length = 50
        if len(self.name) > max_name_length:
            raise StringTooLongError(
                field_name='name',
                max_length=max_name_length,
                current_length=len(self.name),
            )

        if self.planted_at and not self.planted_at.tzinfo:
            raise TimestampWithoutTimezoneError(field_name='planted_at')


@dataclass(kw_only=True)
class CropSearchCriteria:
    """
    Filter parameters for querying :class:`Crop` entities.

    :param name: Common crop name. Case insensitive.
    :type name: str | None
    :param species: Botanical species name. Case insensitive.
    :type species: str | None
    :param description: Description of the crop. Case insensitive.
    :type description: str | None
    :param notes: Notes associated to this crop. Case insensitive.
    :type notes: str | None
    :param planted_at: Timestamp when planted. It searches within 12 hours
                       of this.
    :type planted_at: :class:`datetime.datetime` | None
    :param owner_id: The user this crops belongs to.
                     Relationship to
                     :class:`domain.models.auth.AuthenticatedUser`.
    :type owner_id: str | None
    """

    name: str | None = None
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    planted_at: datetime.datetime | None = None
    owner_id: str | None = None

    def __post_init__(self):
        if self.name:
            self.name = self.name.lower()
        if self.species:
            self.species = self.species.lower()
        if self.description:
            self.description = self.description.lower()
        if self.notes:
            self.notes = self.notes.lower()
        if self.planted_at and not self.planted_at.tzinfo:
            raise TimestampWithoutTimezoneError(field_name='planted_at')
