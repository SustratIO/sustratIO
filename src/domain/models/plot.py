"""
This module contains the definition of the Plot model, which represents a plot
of land in the system. As well as the relationship between plots and crops,
where a plot can have multiple crops associated with it.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from domain.exceptions.validation import (
    OutOfBoundsError,
    TimestampWithoutTimezoneError,
)
from domain.models.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifierMixin,
)

if TYPE_CHECKING:
    import datetime
    import decimal
    import uuid


@dataclass
class Coordinate:
    """
    Represents a geographical coordinate with latitude and longitude.

    :param latitude: Latitude of the coordinate.
    :type latitude: :class:`decimal.Decimal`
    :param longitude: Longitude of the coordinate.
    :type longitude: :class:`decimal.Decimal`
    :param altitude: Altitude of the coordinate.
    :type altitude: :class:`decimal.Decimal` | None
    """

    latitude: decimal.Decimal
    longitude: decimal.Decimal
    altitude: decimal.Decimal | None = None

    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise OutOfBoundsError(
                field_name='latitude',
                value=str(self.latitude),
            )
        if not (-180 <= self.longitude <= 180):
            raise OutOfBoundsError(
                field_name='longitude',
                value=str(self.longitude),
            )


@dataclass(kw_only=True)
class Plot(UniqueIdentifierMixin, AuditTimestampMixin):
    """
    Represents a plot of land.

    :param name: Name of the plot.
    :type name: str
    :param description: Description of the plot.
    :type description: str | None
    :param coordinate: Geographical coordinate of the plot.
    :type coordinate: :class:`Coordinate` | None
    :param owner_id: The user this plot belongs to.
    :type owner_id: str
    """

    name: str
    description: str | None = None
    coordinate: Coordinate | None = None
    owner_id: str


@dataclass(kw_only=True)
class PlotSearchCriteria:
    """
    Represents criteria for searching :class:`Plot` entities.

    :name: The name of the plot to search for.
    :type name: str | None
    :description: The description of the plot to search for.
    :type description: str | None
    :coordinate: The geographical coordinate of the plot to search for.
    :type coordinate: :class:`Coordinate` | None
    :owner_id: The user ID of the plot to search for.
    :type owner_id: str | None
    """

    name: str | None = None
    description: str | None = None
    coordinate: Coordinate | None = None
    owner_id: str | None = None

    def __pos_init__(self):
        # Criteria is fuzzy, so string are lowercase
        if self.name:
            self.name = self.name.lower()
        if self.description:
            self.description = self.description.lower()


@dataclass
class PlotAssignment(UniqueIdentifierMixin, AuditTimestampMixin):
    """
    Represents the assignment of a plot to a crop.

    :param plot_id: The ID of the plot.
    :type plot_id: :class:`uuid.UUID`
    :param crop_id: The ID of the crop.
    :type crop_id: :class:`uuid.UUID`
    :param planted_at: The timestamp when the crop was planted in the plot.
    :type planted_at: :class:`datetime.datetime`
    """

    plot_id: uuid.UUID
    crop_id: uuid.UUID
    planted_at: datetime.datetime

    def __post_init__(self):
        if self.planted_at and not self.planted_at.tzinfo:
            raise TimestampWithoutTimezoneError(field_name='planted_at')
