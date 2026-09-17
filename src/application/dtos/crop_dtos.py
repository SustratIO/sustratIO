from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime


@dataclass(
    frozen=True,
    kw_only=True,
)
class CreateCropInput:
    """
    Data required to create a crop on the use case.

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
    """

    name: str
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    planted_at: datetime.datetime


@dataclass(
    frozen=True,
    kw_only=True,
)
class UpdateCropInput:
    """
    Data required to update a crop on the use case.

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
    """

    name: str | None = None
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    planted_at: datetime.datetime | None = None
