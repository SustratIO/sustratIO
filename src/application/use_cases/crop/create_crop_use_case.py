from typing import TYPE_CHECKING

from domain.exceptions.auth import PermissionDeniedException
from domain.models.auth import Permission
from domain.models.crop import Crop

if TYPE_CHECKING:
    from domain.models.auth import AuthenticatedUser
    from domain.ports.repositories.crop_repository import CropRepositoryPort


class CreateCropUseCase:
    """
    Use case for creating a crop.
    """

    def __init__(self, repo: CropRepositoryPort):
        self.repo = repo

    async def execute(
        self,
        name: str,
        unique_name: str | None,
        description: str | None,
        notes: str | None,
        user: AuthenticatedUser,
    ) -> Crop:
        if Permission.WRITE_CROP not in user.permissions:
            raise PermissionDeniedException(
                "User doesn't have write permissions for crops."
            )

        new_crop = Crop(
            name=name,
            unique_name=unique_name,
            description=description,
            notes=notes,
            owner_id=user.id,
        )
        crop = await self.repo.save(crop=new_crop)

        return crop
