from typing import TYPE_CHECKING

import pytest
from unittest import mock

from application.use_cases.crop.get_crop_use_case import GetCropUseCase

if TYPE_CHECKING:
    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory
    from tests.factories.crop_factory import CropFactory

    from domain.models.auth import AuthenticatedUser
    from domain.models.crop import Crop


pytestmark = [
    pytest.mark.unit,
    pytest.mark.use_case,
    pytest.mark.crop,
]


@pytest.mark.asyncio
async def test_get_crop_execute_raises_entry_not_found_exception(
    in_memory_crop_repo,
    authenticated_user: AuthenticatedUser,
    faker: Faker,
):
    from domain.exceptions.repository import EntityNotFoundException

    use_case = GetCropUseCase(repo=in_memory_crop_repo)

    with pytest.raises(EntityNotFoundException, match='Crop not found.'):
        await use_case.execute(
            faker.uuid4(cast_to=None),
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_get_crop_execute_raises_permission_denied_exception(
    in_memory_crop_repo,
    crop: Crop,
    authenticated_user_factory: type[AuthenticatedUserFactory],
):
    in_memory_crop_repo.get_by_id = mock.AsyncMock(return_value=crop)
    use_case = GetCropUseCase(repo=in_memory_crop_repo)
    authenticated_user = authenticated_user_factory(permissions=set())

    from domain.exceptions.auth import PermissionDeniedException

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have read permissions for this crop.",
    ):
        await use_case.execute(
            identifier=crop.id,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_get_crop_execute_ok(
    in_memory_crop_repo,
    crop_factory: type[CropFactory],
    authenticated_user: AuthenticatedUser,
):
    crop = crop_factory(owner_id=authenticated_user.id)
    in_memory_crop_repo.get_by_id = mock.AsyncMock(return_value=crop)
    use_case = GetCropUseCase(repo=in_memory_crop_repo)

    crop = await use_case.execute(
        identifier=crop.id,
        user=authenticated_user,
    )

    assert crop is not None
