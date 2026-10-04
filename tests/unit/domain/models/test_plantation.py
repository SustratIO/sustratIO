from typing import TYPE_CHECKING

import pytest

from domain.models.plantation import Plantation

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


def test_create_plantation_ok(
    faker: Faker,
):
    Plantation(
        name=faker.name(),
        owner_id=faker.uuid4(cast_to=str),
    )
