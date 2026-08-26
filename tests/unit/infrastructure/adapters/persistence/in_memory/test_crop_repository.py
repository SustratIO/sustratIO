from typing import TYPE_CHECKING

import pytest

from infrastructure.adapters.persistence.in_memory.crop_repository import (
    InMemoryCropRepository,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from faker import Faker

    from domain.models.crop import Crop

    from infrastructure.adapters.persistence.in_memory.connection import (
        Database,
    )

pytestmark = [
    pytest.mark.unit,
    pytest.mark.in_memory,
]


@pytest.fixture(autouse=True)
def dummy_in_memory_db(monkeypatch) -> Generator[Database]:
    dummy_db: Database = {
        'crops': {},
    }

    monkeypatch.setattr(
        'infrastructure.adapters.persistence.in_memory.connection.DATABASE',
        dummy_db,
    )

    yield dummy_db


def test_non_existent_crops_namespace(
    dummy_in_memory_db,
):
    del dummy_in_memory_db['crops']

    from domain.exceptions.repository import RepositoryDataAccessException

    with pytest.raises(
        RepositoryDataAccessException,
        match=r"'crops' not in in-memory database\.",
    ):
        InMemoryCropRepository()


@pytest.mark.asyncio
async def test_save_crop_success(
    dummy_in_memory_db,
    crop: Crop,
):
    repo = InMemoryCropRepository()

    crop = await repo.save(crop=crop)

    assert len(dummy_in_memory_db['crops']) == 1
    assert dummy_in_memory_db['crops'].get(crop.id) is not None


@pytest.mark.asyncio
async def test_get_crop_by_id_not_found(
    faker: Faker,
):
    repo = InMemoryCropRepository()

    crop = await repo.get_by_id(
        identifier=faker.uuid4(cast_to=None),
    )

    assert crop is None


@pytest.mark.asyncio
async def test_get_crop_by_id_success(
    crop: Crop,
):
    repo = InMemoryCropRepository()

    await repo.save(crop=crop)

    found_crop = await repo.get_by_id(
        identifier=crop.id,
    )

    assert crop is found_crop
