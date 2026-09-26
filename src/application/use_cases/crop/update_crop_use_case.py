import datetime
from typing import TYPE_CHECKING

from domain.exceptions.auth import PermissionDeniedException
from domain.exceptions.repository import EntityNotFoundException
from domain.models.auth import Permission
from domain.models.crop import Crop

if TYPE_CHECKING:
    import uuid

    from domain.models.auth import AuthenticatedUser
    from domain.ports.repositories.crop_repository import CropRepositoryPort

    from application.dtos.crop_dtos import UpdateCropInput


class UpdateCropUseCase:
    """
    Updates the crop if found with the given data.
    """

    def __init__(self, repo: CropRepositoryPort):
        self.repo = repo

    async def execute(
        self,
        identifier: uuid.UUID,
        input_data: UpdateCropInput,
        user: AuthenticatedUser,
    ) -> Crop:
        """
        Updates the crop with the given data if found.

        :param identifier: The crop identifier.
        :type identifier: :class:`uuid.UUID`
        :param input_data: The data to update the crop with.
        :type input_data: :class:`UpdateCropInput`
        :param user: The authenticated user.
        :type user: :class:`AuthenticatedUser`
        :return: The updated crop.
        :rtype: :class:`Crop`
        """

        can_read_crops = (
            user.has_permission(Permission.READ_CROPS)
        ) or user.has_permission(Permission.READ_ALL)

        if not can_read_crops:
            raise PermissionDeniedException(
                "User doesn't have read permissions for this crop."
            )

        can_write_crops = (
            user.has_permission(Permission.WRITE_CROPS)
        ) or user.has_permission(Permission.WRITE_ALL)

        if not can_write_crops:
            raise PermissionDeniedException(
                "User doesn't have write permissions for this crop."
            )

        crop = await self.repo.find_one(identifier=identifier)

        if not crop:
            raise EntityNotFoundException('Crop not found.')

        can_update_crop = (
            crop.owner_id == user.id
            and user.has_permission(Permission.WRITE_CROPS)
        ) or user.has_permission(Permission.WRITE_ALL)

        if not can_update_crop:
            raise PermissionDeniedException(
                "User doesn't have ownership of this crop."
            )

        to_update_crop = Crop(
            id=crop.id,
            created_at=crop.created_at,
            updated_at=datetime.datetime.now(tz=datetime.UTC),
            name=input_data.name or crop.name,
            species=input_data.species or crop.species,
            description=input_data.description or crop.description,
            notes=input_data.notes or crop.notes,
            planted_at=input_data.planted_at or crop.planted_at,
            owner_id=crop.owner_id,
        )
        updated_crop = await self.repo.save(crop=to_update_crop)

        return updated_crop
