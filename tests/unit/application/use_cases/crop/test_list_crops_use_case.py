from typing import TYPE_CHECKING

import pytest

from domain.models.crop import CropSearchCriteria

from application.use_cases.crop.list_crops_use_case import ListCropsUseCase

if TYPE_CHECKING:
    from collections.abc import Generator

    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory
    from tests.factories.crop_factory import CropFactory

    from domain.models.auth import AuthenticatedUser

pytestmark = [
    pytest.mark.unit,
    pytest.mark.use_case,
    pytest.mark.crop,
]


@pytest.fixture
def in_memory_repo_use_case(
    in_memory_crop_repo,
) -> Generator[ListCropsUseCase]:
    use_case = ListCropsUseCase(repo=in_memory_crop_repo)

    yield use_case


@pytest.mark.asyncio
async def test_execute_without_permissions_raises_permission_denied_exception(
    authenticated_user_factory: type[AuthenticatedUserFactory],
    in_memory_repo_use_case,
    faker: Faker,
):
    from domain.exceptions.auth import PermissionDeniedException

    user_without_perm = authenticated_user_factory.build(
        permissions=set(),
    )

    with pytest.raises(
        PermissionDeniedException,
        match="User doesn't have read permissions on crops.",
    ):
        await in_memory_repo_use_case.execute(
            criteria=CropSearchCriteria(),
            limit=faker.pyint(),
            user=user_without_perm,
        )


@pytest.mark.asyncio
async def test_execute_required_fields_only_ok(
    crop_factory: type[CropFactory],
    in_memory_crop_repo,
    in_memory_repo_use_case,
    authenticated_user: AuthenticatedUser,
):
    n_entries = 25
    for crop in crop_factory.build_batch(
        size=n_entries,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=crop)

    limit = 50
    paginated_crops = await in_memory_repo_use_case.execute(
        criteria=CropSearchCriteria(),
        limit=limit,
        user=authenticated_user,
    )

    assert len(paginated_crops.items) == n_entries


@pytest.mark.asyncio
async def test_execute_all_fields_ok(
    crop_factory: type[CropFactory],
    in_memory_crop_repo,
    faker: Faker,
    in_memory_repo_use_case,
    authenticated_user: AuthenticatedUser,
):
    for to_create_crop in crop_factory.build_batch(
        size=25,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=to_create_crop)
    await in_memory_crop_repo.save(
        crop=crop_factory.build(
            name='Basil',
            species='Ocimum basilicum',
            description='Basil (Ocimum basilicum), also called great basil, is a culinary herb...',
            notes='Needs water.',
            owner_id=authenticated_user.id,
        )
    )

    limit = 50
    paginated_crops = await in_memory_repo_use_case.execute(
        criteria=CropSearchCriteria(
            name='Basil',
            species='basilicum',
            description='also called great basil',
            notes='water',
        ),
        limit=limit,
        user=authenticated_user,
    )

    assert len(paginated_crops.items) == 1


@pytest.mark.asyncio
async def test_execute_user_only_sees_owned_entries_ok(
    crop_factory: type[CropFactory],
    in_memory_crop_repo,
    in_memory_repo_use_case,
    authenticated_user: AuthenticatedUser,
):
    for to_create_crop in crop_factory.build_batch(
        size=25,
    ):
        await in_memory_crop_repo.save(crop=to_create_crop)
    await in_memory_crop_repo.save(
        crop=crop_factory.build(
            owner_id=authenticated_user.id,
        ),
    )

    limit = 50
    paginated_crops = await in_memory_repo_use_case.execute(
        criteria=CropSearchCriteria(),
        limit=limit,
        user=authenticated_user,
    )

    assert len(paginated_crops.items) == 1
