import datetime
from typing import TYPE_CHECKING

import pytest

from domain.exceptions.validation import StringTooLongError
from domain.models.crop import Crop

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


def test_name_too_long_raises_string_too_long_error(
    faker: Faker,
):
    with pytest.raises(
        StringTooLongError,
        match=(
            r"Field 'name' exceeded maximum allowed characters \(50\). "
            'Current: 300'
        ),
    ):
        Crop(
            name=faker.pystr(min_chars=300, max_chars=300),
            planted_at=faker.past_datetime(tzinfo=datetime.UTC),
            owner_id=faker.uuid4(cast_to=str),
        )


def test_required_data_only_ok(
    faker: Faker,
):
    Crop(
        name=faker.pystr(max_chars=50),
        planted_at=faker.past_datetime(tzinfo=datetime.UTC),
        owner_id=faker.uuid4(cast_to=str),
    )


def test_all_fields_ok(
    faker: Faker,
):
    Crop(
        name=faker.pystr(max_chars=50),
        species=faker.pystr(),
        description=faker.sentence(),
        notes=faker.sentence(),
        planted_at=faker.past_datetime(tzinfo=datetime.UTC),
        owner_id=faker.uuid4(cast_to=str),
    )
