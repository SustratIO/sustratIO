import datetime
import logging
import uuid
from typing import TYPE_CHECKING

from domain.exceptions.repository import RepositoryDataAccessException
from domain.models.crop import Crop, CropSearchCriteria
from domain.models.pagination import CursorPage
from domain.ports.repositories.crop_repository import CropRepositoryPort

if TYPE_CHECKING:
    from domain.models.crop import Crop
    from domain.models.pagination import CursorData

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
        if crop.id in self._storage:
            crop.updated_at = datetime.datetime.now(
                tz=datetime.UTC,
            )

        self._storage[crop.id] = crop

        return self._storage[crop.id]

    async def find_one(self, identifier: uuid.UUID) -> Crop | None:
        return self._storage.get(identifier, None)

    async def find_many(
        self,
        filters: CropSearchCriteria,
        limit: int = 100,
        cursor: str | None = None,
    ) -> CursorPage[Crop]:
        crops = self._storage.values()

        if filters.name:
            crops = [
                crop for crop in crops if filters.name in crop.name.lower()
            ]

        if filters.species:
            crops = [
                crop
                for crop in crops
                if crop.species and filters.species in crop.species.lower()
            ]

        if filters.description:
            crops = [
                crop
                for crop in crops
                if crop.description
                and filters.description in crop.description.lower()
            ]

        if filters.notes:
            crops = [
                crop
                for crop in crops
                if crop.notes and filters.notes in crop.notes.lower()
            ]

        if filters.planted_at:
            # Fuzzy match: crop.planted_at is within 12 hours of filters.planted_at
            margin = datetime.timedelta(hours=12)
            crops = [
                crop
                for crop in crops
                if abs(crop.planted_at - filters.planted_at) <= margin
            ]

        if filters.owner_id:
            crops = [
                crop for crop in crops if crop.owner_id == filters.owner_id
            ]

        crops = sorted(
            crops,
            key=lambda crop: (
                crop.created_at,
                crop.id,
            ),
            reverse=True,
        )

        if cursor:
            cursor_data = CursorPage.decode_cursor(cursor=cursor)
            crops = [
                crop
                for crop in crops
                if (crop.created_at, crop.id.hex)
                < (cursor_data['timestamp'], cursor_data['id'])
            ]

        # Slice the results based on the limit + 1 to detect if there's more than limit
        paged_crops = crops[: limit + 1]

        # Determine the next cursor
        if len(paged_crops) > limit:
            # Removing the last entry
            paged_crops = paged_crops[:limit]

            # The last crop is our cursor
            last_crop = paged_crops[-1]
            next_cursor_data: CursorData = {
                'id': str(last_crop.id),
                'timestamp': last_crop.created_at,
            }
            next_cursor = CursorPage.encode_cursor(
                cursor_data=next_cursor_data,
            )
        else:
            next_cursor = None

        return CursorPage(
            items=paged_crops,
            next_cursor=next_cursor,
        )
