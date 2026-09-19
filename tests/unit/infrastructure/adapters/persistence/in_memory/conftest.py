from typing import TYPE_CHECKING

import pytest

from infrastructure.adapters.persistence.in_memory.crop_repository import (
    InMemoryCropRepository,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from infrastructure.adapters.persistence.in_memory.connection import (
        Database,
    )


@pytest.fixture
def dummy_in_memory_db(monkeypatch) -> Generator[Database]:
    """
    Generates a dummy in-memory database so data is not shared across tests.
    """

    dummy_db: Database = {
        'crops': {},
    }

    monkeypatch.setattr(
        'infrastructure.adapters.persistence.in_memory.connection.DATABASE',
        dummy_db,
    )

    yield dummy_db


@pytest.fixture
def in_memory_repository(dummy_in_memory_db):
    """
    Given the in-memory database at :method:`dummy_in_memory_db`.
    """

    repo = InMemoryCropRepository()

    yield repo
