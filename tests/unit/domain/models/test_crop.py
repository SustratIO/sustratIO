from typing import TYPE_CHECKING

import pytest

from domain.exceptions.validation import (
    StringTooLongError,
)
from domain.models.crop import Crop, CropSearchCriteria

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


class TestCrop:
    def test_name_too_long_raises_string_too_long_error(
        self,
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
                owner_id=faker.uuid4(cast_to=str),
            )

    def test_required_data_only_success(
        self,
        faker: Faker,
    ):
        Crop(
            name=faker.pystr(max_chars=50),
            owner_id=faker.uuid4(cast_to=str),
        )

    def test_all_fields_success(
        self,
        faker: Faker,
    ):
        Crop(
            name=faker.pystr(max_chars=50),
            species=faker.pystr(),
            description=faker.sentence(),
            notes=faker.sentence(),
            owner_id=faker.uuid4(cast_to=str),
        )


class TestCropSearchCriteria:
    def test_required_data_only_success(
        self,
    ):
        CropSearchCriteria()

    def test_all_fields_success(
        self,
        faker: Faker,
    ):
        CropSearchCriteria(
            name=faker.pystr(max_chars=50),
            species=faker.pystr(),
            description=faker.sentence(),
            notes=faker.sentence(),
            owner_id=faker.uuid4(cast_to=str),
        )

    def test_text_fields_are_lowercase(self, faker: Faker):
        criteria = CropSearchCriteria(
            name='Basil',
            species='Ocimum basilicum',
            description='Basil (Ocimum basilicum), also called great basil, is a culinary herb...',
            notes='Needs water.',
        )

        assert criteria.name == 'basil'
        assert criteria.species == 'ocimum basilicum'
        assert (
            criteria.description
            == 'basil (ocimum basilicum), also called great basil, is a culinary herb...'
        )
        assert criteria.notes == 'needs water.'
