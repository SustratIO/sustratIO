from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import uuid

    from domain.models.crop import Crop


class CropRepositoryPort(Protocol):
    """
    Defines domain logic for interacting with the crop entity.
    """

    async def save(self, crop: Crop) -> Crop:
        """
        Persists the given :class:`Crop` object in the database.

        :param crop: The crop object to store.
        :type crop: :class:`Crop`
        :return: The persisted crop object (with the relevant permuted data if
                 any)
        :rtype: :class:`Crop`
        """
        ...

    async def get_by_id(self, identifier: uuid.UUID) -> Crop | None:
        """
        Given a unique identifier, returns the associated crop.

        :param identifier: The unique identifier for the crop.
        :type identifier: :class:`uuid.UUID`
        :return: Crop object if found, None otherwise.
        :rtype: :class:`Crop` | None
        """
        ...
