from dataclasses import dataclass

from domain.models.crop import SowingPeriod


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
    :param sowing_season_start: Start of the sowing season.
    :type sowing_season_start: :class:`SowingPeriod` | None
    :param sowing_season_end: End of the sowing season.
    :type sowing_season_end: :class:`SowingPeriod` | None
    """

    name: str
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    sowing_season_start: SowingPeriod | None = None
    sowing_season_end: SowingPeriod | None = None


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
    :param sowing_season_start: Start of the sowing season.
    :type sowing_season_start: :class:`SowingPeriod` | None
    :param sowing_season_end: End of the sowing season.
    :type sowing_season_end: :class:`SowingPeriod` | None
    """

    name: str | None = None
    species: str | None = None
    description: str | None = None
    notes: str | None = None
    sowing_season_start: SowingPeriod | None = None
    sowing_season_end: SowingPeriod | None = None
