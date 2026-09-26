from typing import TYPE_CHECKING

from domain.exceptions.auth import PermissionDeniedException
from domain.models.auth import Permission

if TYPE_CHECKING:
    from domain.models.auth import AuthenticatedUser
    from domain.models.crop import Crop, CropSearchCriteria
    from domain.models.pagination import CursorPage
    from domain.ports.repositories.crop_repository import CropRepositoryPort


class ListCropsUseCase:
    """
    Under a search criteria, it list all the crops found for given user.
    """

    def __init__(self, repo: CropRepositoryPort) -> None:
        self.repo = repo

    async def execute(
        self,
        criteria: CropSearchCriteria,
        limit: int,
        user: AuthenticatedUser,
        cursor: str | None = None,
    ) -> CursorPage[Crop]:
        """
        Given `criteria` it returns a paginated list of items.

        :param criteria: Filters the list of items meet.
        :type criteria: :class:`CropSearchCriteria`
        :param limit: Number of entries to return.
        :type limit: int
        :return: Paginated list of :class:`Crop`.
        :rtype: :class:`CursorPage`
        """

        can_read_crops = (
            user.has_permission(Permission.READ_CROPS)
        ) or user.has_permission(Permission.READ_ALL)

        if not can_read_crops:
            raise PermissionDeniedException(
                "User doesn't have read permissions on crops."
            )

        # Enforce that the user can only query their own crops
        criteria.owner_id = user.id

        crops = await self.repo.find_many(
            filters=criteria,
            limit=limit,
            cursor=cursor,
        )
        return crops
