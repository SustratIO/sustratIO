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
        if Permission.WRITE_CROP not in user.permissions:
            raise PermissionDeniedException(
                "User doesn't have write permissions for crops."
            )

        new_crop = Crop(
            name=input_data.name,
            species=input_data.species,
            description=input_data.description,
            notes=input_data.notes,
            planted_at=input_data.planted_at,
            owner_id=user.id,
        )
        crop = await self.repo.save(crop=new_crop)

        return crop
