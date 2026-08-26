import uuid
from typing import TYPE_CHECKING

from domain.exceptions.auth import PermissionDeniedException
from domain.exceptions.repository import EntityNotFoundException
from domain.models.auth import Permission

if TYPE_CHECKING:
    from domain.models.auth import AuthenticatedUser
    from domain.models.crop import Crop
    from domain.ports.repositories.crop_repository import CropRepositoryPort


class GetCropUseCase:
    """
    Use case for retrieving a single crop by given id.
    """

    def __init__(self, repo: CropRepositoryPort):
        self.repo = repo

    async def execute(
        self,
        identifier: uuid.UUID,
        user: AuthenticatedUser,
    ) -> Crop:
        crop = await self.repo.get_by_id(identifier=identifier)

        if not crop:
            raise EntityNotFoundException('Crop not found.')

        if not (
            crop.owner_id == user.id
            and Permission.READ_CROP in user.permissions
        ):
            raise PermissionDeniedException(
                "User doesn't have read permissions for this crop."
            )

        return crop
