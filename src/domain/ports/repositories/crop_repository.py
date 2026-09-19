"""
Embodies the ports to interact with the crops entities storage.
"""

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import uuid

    from domain.models.crop import Crop, CropSearchCriteria
    from domain.models.pagination import CursorPage


class CropRepositoryPort(Protocol):
    """
    Defines domain logic for interacting with the crop entity.
    """

    async def save(
        self,
        crop: Crop,
    ) -> Crop:
        """
        Persists or updates the given :class:`Crop` object in the database.

        :param crop: The crop object to store or update.
        :type crop: :class:`Crop`
        :return: The persisted crop object (with the relevant permuted data if
                 any)
        :rtype: :class:`Crop`
        """
        ...

    async def find_one(
        self,
        identifier: uuid.UUID,
    ) -> Crop | None:
        """
        Given a unique identifier, returns the associated crop.

        :param identifier: The unique identifier for the crop.
        :type identifier: :class:`uuid.UUID`
        :return: Crop object if found, None otherwise.
        :rtype: :class:`Crop` | None
        """
        ...

    async def find_many(
        self,
        filters: CropSearchCriteria,
        limit: int = 100,
        cursor: str | None = None,
    ) -> CursorPage[Crop]:
        """
        Given the filters, returns a paginated list of crops.

        :param filters: Criteria to filter by.
        :type filters: :class:`CropSearchCriteria`
        :param limit: Number of crops to return.
        :type limit: int
        :return: List of crops under cursor pagination.
        :rtype: :class:`CursorPage`
        """
        ...
