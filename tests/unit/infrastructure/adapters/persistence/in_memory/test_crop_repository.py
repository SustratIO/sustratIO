import datetime
from typing import TYPE_CHECKING

import pytest

from domain.models.crop import CropSearchCriteria

if TYPE_CHECKING:
    from faker import Faker
    from tests.factories.crop_factory import CropFactory

    from domain.models.crop import Crop


pytestmark = [
    pytest.mark.unit,
    pytest.mark.in_memory,
]


def test_non_existent_crops_namespace(
    dummy_in_memory_db,
):
    del dummy_in_memory_db['crops']

    from domain.exceptions.repository import RepositoryDataAccessException

    from infrastructure.adapters.persistence.in_memory.crop_repository import (
        InMemoryCropRepository,
    )

    with pytest.raises(
        RepositoryDataAccessException,
        match=r"'crops' not in in-memory database\.",
    ):
        InMemoryCropRepository()


@pytest.mark.asyncio
async def test_save_crop_success(
    in_memory_repository,
    dummy_in_memory_db,
    crop: Crop,
):
    crop = await in_memory_repository.save(crop=crop)

    assert len(dummy_in_memory_db['crops']) == 1
    assert dummy_in_memory_db['crops'].get(crop.id) is not None


@pytest.mark.asyncio
async def test_save_on_existent_updates_success(
    in_memory_repository,
    crop: Crop,
    crop_factory: type[CropFactory],
):
    await in_memory_repository.save(crop)

    updated_crop: Crop = crop_factory.build(
        id=crop.id,
        name='Updated!',
    )
    new_crop = await in_memory_repository.save(updated_crop)

    # Since `crop` is an object, the reference in memory should be the same
    assert new_crop.id == crop.id
    assert new_crop.name == updated_crop.name
    assert new_crop.updated_at is not None


@pytest.mark.asyncio
async def test_find_one_not_found(
    in_memory_repository,
    faker: Faker,
):
    crop = await in_memory_repository.find_one(
        identifier=faker.uuid4(cast_to=None),
    )

    assert crop is None


@pytest.mark.asyncio
async def test_find_one_success(
    in_memory_repository,
    crop: Crop,
):
    await in_memory_repository.save(crop=crop)

    found_crop = await in_memory_repository.find_one(
        identifier=crop.id,
    )

    assert crop is found_crop


@pytest.mark.asyncio
async def test_find_many_without_filters_empty_items_less_than_limit_success(
    in_memory_repository,
):
    paginated_crops = await in_memory_repository.find_many(
        filters=CropSearchCriteria()
    )

    assert len(paginated_crops.items) == 0
    assert paginated_crops.next_cursor is None


@pytest.mark.asyncio
async def test_find_many_without_filters_items_less_than_limit_success(
    in_memory_repository,
    crop_factory: type[CropFactory],
):
    n_items = 15
    for crop in crop_factory.build_batch(size=n_items):
        await in_memory_repository.save(crop)

    paginated_crops = await in_memory_repository.find_many(
        filters=CropSearchCriteria(),
        limit=n_items,
    )

    assert len(paginated_crops.items) == n_items
    assert paginated_crops.next_cursor is None


@pytest.mark.asyncio
async def test_find_many_without_filters_items_more_than_limit_success(
    in_memory_repository,
    crop_factory: type[CropFactory],
):
    n_items = 15
    for crop in crop_factory.build_batch(size=n_items):
        await in_memory_repository.save(crop)

    limit = 10
    paginated_crops = await in_memory_repository.find_many(
        filters=CropSearchCriteria(),
        limit=limit,
    )

    assert len(paginated_crops.items) == limit
    assert paginated_crops.next_cursor is not None


@pytest.mark.asyncio
async def test_find_many_without_filters_cursor_success(
    in_memory_repository,
    crop_factory: type[CropFactory],
):
    for crop in crop_factory.build_batch(size=3):
        await in_memory_repository.save(crop=crop)

    # We just replicate the exact behavior is expected to have
    paginated_crops_first_page = await in_memory_repository.find_many(
        filters=CropSearchCriteria(),
        limit=1,
        cursor=None,
    )
    paginated_crops = await in_memory_repository.find_many(
        filters=CropSearchCriteria(),
        limit=10,
        cursor=paginated_crops_first_page.next_cursor,
    )

    assert len(paginated_crops.items) == 2
    assert paginated_crops.next_cursor is None


@pytest.mark.asyncio
async def test_find_many_with_filters_success(
    in_memory_repository,
    crop_factory: type[CropFactory],
    faker: Faker,
):
    # We create random entries to ensure none of them are returned
    n_items = 15
    for crop in crop_factory.build_batch(size=n_items):
        await in_memory_repository.save(crop=crop)

    owner_id = faker.uuid4(cast_to=str)
    crop: Crop = crop_factory.build(
        name='Green Basil',
        species='Ocimum basilicum',
        description='Basil (Ocimum basilicum), also called great basil, is a culinary herb...',
        notes='Needs water.',
        planted_at=datetime.datetime(
            year=1998,
            month=7,
            day=14,
            hour=8,
            minute=32,
            second=0,
            microsecond=0,
            tzinfo=datetime.UTC,
        ),
        owner_id=owner_id,
    )
    await in_memory_repository.save(crop=crop)

    # Fuzzy criteria
    criteria = CropSearchCriteria(
        name='basil',
        species='basilicum',
        description='also called great basil',
        notes='needs water',
        planted_at=datetime.datetime(
            year=1998,
            month=7,
            day=14,
            hour=12,
            minute=0,
            tzinfo=datetime.UTC,
        ),
        owner_id=owner_id,
    )

    paginated_crops = await in_memory_repository.find_many(
        filters=criteria,
        limit=10,
        cursor=None,
    )

    assert len(paginated_crops.items) == 1
    assert paginated_crops.next_cursor is None
