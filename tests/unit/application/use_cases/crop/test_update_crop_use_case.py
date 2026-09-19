import datetime
from typing import TYPE_CHECKING

import pytest
from unittest import mock

from domain.models.auth import Permission

from application.dtos.crop_dtos import UpdateCropInput
from application.use_cases.crop.update_crop_use_case import UpdateCropUseCase

if TYPE_CHECKING:
    from collections.abc import Generator

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


@pytest.fixture
def in_memory_repo_use_case(
    in_memory_crop_repo,
) -> Generator[UpdateCropUseCase]:
    use_case = UpdateCropUseCase(repo=in_memory_crop_repo)

    yield use_case


@pytest.mark.asyncio
async def test_execute_not_found_raises_entry_not_found_exception(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_repo_use_case,
    faker: Faker,
):
    authenticated_user = authenticated_user_factory.build(
        permissions={
            Permission.READ_CROP,
            Permission.WRITE_CROP,
        },
    )
    input_data = UpdateCropInput()

    from domain.exceptions.repository import EntityNotFoundException

    with pytest.raises(EntityNotFoundException, match='Crop not found.'):
        await in_memory_repo_use_case.execute(
            identifier=faker.uuid4(cast_to=None),
            input_data=input_data,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_execute_user_without_read_permission_raises_permission_denied_exception(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_repo_use_case,
    faker: Faker,
):
    authenticated_user = authenticated_user_factory.build(
        permissions={
            Permission.WRITE_CROP,
        },
    )
    input_data = UpdateCropInput()

    from domain.exceptions.auth import PermissionDeniedException

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have read permissions for this crop.",
    ):
        await in_memory_repo_use_case.execute(
            identifier=faker.uuid4(cast_to=None),
            input_data=input_data,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_execute_without_write_permission_raises_permission_denied_exception(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_crop_repo,
    crop_factory: type[CropFactory],
    in_memory_repo_use_case,
    faker: Faker,
):
    authenticated_user: AuthenticatedUser = authenticated_user_factory.build(
        permissions={
            Permission.READ_CROP,
        },
    )
    in_memory_crop_repo.find_one = mock.AsyncMock(
        return_value=crop_factory.build(owner_id=authenticated_user.id),
    )
    input_data = UpdateCropInput()

    from domain.exceptions.auth import PermissionDeniedException

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have write permissions for this crop.",
    ):
        await in_memory_repo_use_case.execute(
            identifier=faker.uuid4(cast_to=None),
            input_data=input_data,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_execute_user_without_ownership_raises_permission_denied_exception(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_crop_repo,
    crop: Crop,
    in_memory_repo_use_case,
):
    authenticated_user: AuthenticatedUser = authenticated_user_factory.build(
        permissions={
            Permission.READ_CROP,
            Permission.WRITE_CROP,
        },
    )
    in_memory_crop_repo.find_one = mock.AsyncMock(
        return_value=crop,
    )
    input_data = UpdateCropInput()

    from domain.exceptions.auth import PermissionDeniedException

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have ownership of this crop.",
    ):
        await in_memory_repo_use_case.execute(
            identifier=crop.id,
            input_data=input_data,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_execute_ok(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_crop_repo,
    crop_factory: type[CropFactory],
    in_memory_repo_use_case,
):
    authenticated_user: AuthenticatedUser = authenticated_user_factory.build(
        permissions={
            Permission.READ_CROP,
            Permission.WRITE_CROP,
        },
    )
    crop = crop_factory.build(owner_id=authenticated_user.id)
    await in_memory_crop_repo.save(crop=crop)
    input_data = UpdateCropInput(name='New name')

    new_crop = await in_memory_repo_use_case.execute(
        identifier=crop.id,
        input_data=input_data,
        user=authenticated_user,
    )

    assert new_crop is not None
    assert (
        datetime.datetime.now(tz=datetime.UTC) - new_crop.updated_at
    ) < datetime.timedelta(seconds=2)
