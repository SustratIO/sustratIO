import datetime
from typing import TYPE_CHECKING

import pytest

from application.dtos.crop_dtos import CreateCropInput
from application.use_cases.crop.create_crop_use_case import CreateCropUseCase

if TYPE_CHECKING:
    from collections.abc import Generator

    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory

    from domain.models.auth import AuthenticatedUser


pytestmark = [
    pytest.mark.unit,
    pytest.mark.use_case,
    pytest.mark.crop,
]


@pytest.fixture
def in_memory_repo_use_case(
    in_memory_crop_repo,
) -> Generator[CreateCropUseCase]:
    use_case = CreateCropUseCase(repo=in_memory_crop_repo)

    yield use_case


@pytest.mark.asyncio
async def test_execute_user_without_write_permission_raises_permission_denied_exception(
    faker: Faker,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_repo_use_case,
):
    from domain.exceptions.auth import PermissionDeniedException

    dummy_authenticated_user = authenticated_user_factory.build(
        permissions=set(),
    )
    input_data = CreateCropInput(
        name=faker.name(),
        species=None,
        description=None,
        notes=None,
        planted_at=faker.date_time(tzinfo=datetime.UTC),
    )

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have write permissions for crops.",
    ):
        await in_memory_repo_use_case.execute(
            input_data=input_data,
            user=dummy_authenticated_user,
        )


@pytest.mark.asyncio
async def test_execute_all_fields_ok(
    authenticated_user: AuthenticatedUser,
    faker: Faker,
    in_memory_repo_use_case,
):
    input_data = CreateCropInput(
        name='Basil',
        species='Ocimum basilicum',
        description=(
            'Basil (Ocimum basilicum), also called great basil, is'
            ' a culinary herb of the family Lamiaceae (mints).'
        ),
        notes='Needs water.',
        planted_at=faker.date_time(tzinfo=datetime.UTC),
    )

    crop = await in_memory_repo_use_case.execute(
        input_data=input_data,
        user=authenticated_user,
    )

    assert crop.name == input_data.name
    assert crop.species == input_data.species
    assert crop.description == input_data.description
    assert crop.notes == input_data.notes
    assert crop.owner_id == authenticated_user.id
    assert (
        datetime.datetime.now(tz=datetime.UTC) - crop.created_at
    ) < datetime.timedelta(seconds=2)
    assert crop.updated_at is None


@pytest.mark.asyncio
async def test_execute_required_fields_only_ok(
    authenticated_user: AuthenticatedUser,
    faker: Faker,
    in_memory_repo_use_case,
):
    input_data = CreateCropInput(
        name='Basil',
        species=None,
        description=None,
        notes=None,
        planted_at=faker.date_time(tzinfo=datetime.UTC),
    )

    crop = await in_memory_repo_use_case.execute(
        input_data=input_data,
        user=authenticated_user,
    )

    assert crop.name == input_data.name
    assert crop.species is None
    assert crop.description is None
    assert crop.notes is None
    assert crop.owner_id == authenticated_user.id
    assert (
        datetime.datetime.now(tz=datetime.UTC) - crop.created_at
    ) < datetime.timedelta(seconds=2)
    assert crop.updated_at is None
