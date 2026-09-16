from typing import TYPE_CHECKING

import pytest
from unittest import mock

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
async def test_list_crops_use_case_execute_without_permissions_raises_permission_denied_exception(
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
        match="User doesn't have read permissions crops.",
    ):
        await in_memory_repo_use_case.execute(
            criteria=CropSearchCriteria(),
            limit=faker.pyint(),
            user=user_without_perm,
        )


@pytest.mark.asyncio
async def test_list_crops_use_case_execute_ok(
    crop_factory: type[CropFactory],
    faker: Faker,
    in_memory_crop_repo,
    in_memory_repo_use_case,
    authenticated_user: AuthenticatedUser,
):
    from domain.models.pagination import CursorPage

    limit = 50

    data = CursorPage(
        items=crop_factory.build_batch(
            size=faker.pyint(
                min_value=1,
                max_value=limit,
            ),
        ),
        next_cursor=faker.pystr(),
    )
    in_memory_crop_repo.find_many = mock.AsyncMock(return_value=data)

    crops = await in_memory_repo_use_case.execute(
        criteria=CropSearchCriteria(),
        limit=limit,
        user=authenticated_user,
    )

    assert len(crops.items) <= limit
