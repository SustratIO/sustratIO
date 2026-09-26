"""
The models contained here hold and perform transformations on data regarding
crops.
"""

from dataclasses import dataclass
from enum import IntEnum

from domain.exceptions.validation import (
    StringTooLongError,
)
from domain.models.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifier,
)


class Month(IntEnum):
    """
    Enum for months of the year.
    """

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class Fortnight(IntEnum):
    """
    Enum for the two fortnights of a month.
    """

    FIRST = 1
    SECOND = 2


@dataclass(frozen=True)
class SowingPeriod:
    """
    Represents a sowing period for a crop.

    :param month: Month of the sowing period.
    :type month: :class:`Month`
    :param fortnight: Fortnight of the sowing period.
    :type fortnight: :class:`Fortnight`
    """

    month: Month
    fortnight: Fortnight


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
    :param sowing_season_start: Start of the sowing season.
    :type sowing_season_start: :class:`SowingPeriod` | None
    :param owner_id: The user this crops belongs to.
    :type owner_id: str
    """

    name: str
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    sowing_season_start: SowingPeriod | None = None
    sowing_season_end: SowingPeriod | None = None
    owner_id: str

    def __post_init__(self):
        max_name_length = 50
        if len(self.name) > max_name_length:
            raise StringTooLongError(
                field_name='name',
                max_length=max_name_length,
                current_length=len(self.name),
            )


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
    :param sowing_season_start: Start of the sowing season.
    :type sowing_season_start: :class:`SowingPeriod` | None
    :param sowing_season_end: End of the sowing season.
    :type sowing_season_end: :class:`SowingPeriod` | None
    :param owner_id: The user this crops belongs to.
                     Relationship to
                     :class:`domain.models.auth.AuthenticatedUser`.
    :type owner_id: str | None
    """

    name: str | None = None
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    sowing_season_start: SowingPeriod | None = None
    sowing_season_end: SowingPeriod | None = None
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
