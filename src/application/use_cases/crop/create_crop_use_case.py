from typing import TYPE_CHECKING

from domain.exceptions.auth import PermissionDeniedException
from domain.models.auth import Permission
from domain.models.crop import Crop

if TYPE_CHECKING:
    from domain.models.auth import AuthenticatedUser
    from domain.ports.repositories.crop_repository import CropRepositoryPort

    from application.dtos.crop_dtos import CreateCropInput


class CreateCropUseCase:
    """
    Creates a crop with given data.
    """

    def __init__(self, repo: CropRepositoryPort):
        self.repo = repo

    async def execute(
        self,
        input_data: CreateCropInput,
        user: AuthenticatedUser,
    ) -> Crop:
        can_write_crops = (
            user.has_permission(Permission.WRITE_CROPS)
        ) or user.has_permission(Permission.WRITE_ALL)

        if not can_write_crops:
            raise PermissionDeniedException(
                "User doesn't have write permissions for crops."
            )

        new_crop = Crop(
            name=input_data.name,
            species=input_data.species,
            description=input_data.description,
            notes=input_data.notes,
            sowing_season_start=input_data.sowing_season_start,
            sowing_season_end=input_data.sowing_season_end,
            owner_id=user.id,
        )
        crop = await self.repo.save(crop=new_crop)

        return crop
