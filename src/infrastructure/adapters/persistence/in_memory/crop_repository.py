import logging
import uuid
from typing import TYPE_CHECKING

from domain.exceptions.repository import RepositoryDataAccessException
from domain.ports.repositories.crop_repository import CropRepositoryPort

if TYPE_CHECKING:
    from domain.models.crop import Crop

logger = logging.getLogger(__name__)


class InMemoryCropRepository(CropRepositoryPort):
    def __init__(self) -> None:
        from infrastructure.adapters.persistence.in_memory.connection import (
            DATABASE,
        )

        try:
            self._storage = DATABASE['crops']
        except KeyError:
            raise RepositoryDataAccessException(
                "'crops' not in in-memory database."
            )

    async def save(self, crop: Crop) -> Crop:
        self._storage[crop.id] = crop
        return self._storage[crop.id]

    async def get_by_id(self, identifier: uuid.UUID) -> Crop | None:
        return self._storage.get(identifier, None)
