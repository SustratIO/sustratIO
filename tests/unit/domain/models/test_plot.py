import decimal
from typing import TYPE_CHECKING

import pytest

from domain.exceptions.validation import (
    OutOfBoundsError,
    TimestampWithoutTimezoneError,
)
from domain.models.plot import Coordinate, PlotAssignment

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


def test_coordinate_latitude_set_out_of_bounds_raises_out_of_bounds_error(
    faker: Faker,
):
    with pytest.raises(
        OutOfBoundsError,
        match="Field 'latitude' has an out-of-bounds value: -91",
    ):
        Coordinate(
            latitude=decimal.Decimal(-91),
            longitude=faker.pydecimal(min_value=-180, max_value=180),
        )


def test_coordinate_longitude_set_out_of_bounds_raises_out_of_bounds_error(
    faker: Faker,
):
    with pytest.raises(
        OutOfBoundsError,
        match="Field 'longitude' has an out-of-bounds value: 181",
    ):
        Coordinate(
            latitude=faker.pydecimal(min_value=-90, max_value=90),
            longitude=decimal.Decimal(181),
        )


def test_coordinate_ok(
    faker: Faker,
):
    Coordinate(
        latitude=faker.pydecimal(min_value=-90, max_value=90),
        longitude=faker.pydecimal(min_value=-180, max_value=180),
    )


def test_plot_assignment_planted_at_without_timezone_raises_timestamp_without_timezone_error(
    faker: Faker,
):
    with pytest.raises(
        TimestampWithoutTimezoneError,
        match="Field 'planted_at' doesn't have timezone.",
    ):
        PlotAssignment(
            plot_id=faker.uuid4(cast_to=None),
            crop_id=faker.uuid4(cast_to=None),
            planted_at=faker.date_time(),
        )


def test_plot_assignment_ok(
    faker: Faker,
):
    import datetime

    PlotAssignment(
        plot_id=faker.uuid4(cast_to=None),
        crop_id=faker.uuid4(cast_to=None),
        planted_at=faker.date_time(tzinfo=datetime.UTC),
    )
