from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from application.use_cases.crop.create_crop_use_case import CreateCropUseCase

if TYPE_CHECKING:
    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory

    from domain.models.auth import AuthenticatedUser


pytestmark = [
    pytest.mark.unit,
    pytest.mark.use_case,
    pytest.mark.crop,
]


@pytest.mark.asyncio
async def test_create_crop_execute_raises_permission_denied_exception(
    faker: Faker,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_crop_repo,
):
    use_case = CreateCropUseCase(repo=in_memory_crop_repo)

    from domain.exceptions.auth import PermissionDeniedException

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have write permissions for crops.",
    ):
        dummy_authenticated_user = authenticated_user_factory(
            permissions=set(),
        )
        await use_case.execute(
            name=faker.name(),
            unique_name=None,
            description=None,
            notes=None,
            user=dummy_authenticated_user,
        )


@pytest.mark.asyncio
async def test_create_crop_execute_raises_exception(
    faker: Faker,
    authenticated_user: AuthenticatedUser,
    in_memory_crop_repo,
):
    from unittest import mock

    from domain.exceptions.repository import RepositoryDataAccessException

    in_memory_crop_repo.save = mock.MagicMock(
        side_effect=RepositoryDataAccessException
    )
    use_case = CreateCropUseCase(repo=in_memory_crop_repo)

    with pytest.raises(RepositoryDataAccessException):
        await use_case.execute(
            name=faker.name(),
            unique_name=None,
            description=None,
            notes=None,
            user=authenticated_user,
        )


@pytest.mark.asyncio
async def test_create_crop_execute_all_fields_ok(
    authenticated_user: AuthenticatedUser,
    in_memory_crop_repo,
):
    use_case = CreateCropUseCase(repo=in_memory_crop_repo)

    data = {
        'name': 'Basil',
        'unique_name': 'Ocimum basilicum',
        'description': (
            'Basil (Ocimum basilicum), also called great basil, is'
            ' a culinary herb of the family Lamiaceae (mints).'
        ),
        'notes': 'Needs water.',
    }

    crop = await use_case.execute(
        **data,
        user=authenticated_user,
    )

    assert crop.name == data['name']
    assert crop.unique_name == data['unique_name']
    assert crop.description == data['description']
    assert crop.notes == data['notes']
    assert crop.owner_id == authenticated_user.id
    assert (datetime.now(tz=UTC) - crop.created_at) < timedelta(seconds=2)
    assert crop.updated_at is None


@pytest.mark.asyncio
async def test_create_crop_execute_required_fields_only_ok(
    authenticated_user: AuthenticatedUser,
    in_memory_crop_repo,
):
    use_case = CreateCropUseCase(repo=in_memory_crop_repo)

    data = {
        'name': 'Basil',
    }

    crop = await use_case.execute(
        **data,
        unique_name=None,
        description=None,
        notes=None,
        user=authenticated_user,
    )

    assert crop.name == data['name']
    assert crop.unique_name is None
    assert crop.description is None
    assert crop.notes is None
    assert crop.owner_id == authenticated_user.id
    assert (datetime.now(tz=UTC) - crop.created_at) < timedelta(seconds=2)
    assert crop.updated_at is None
