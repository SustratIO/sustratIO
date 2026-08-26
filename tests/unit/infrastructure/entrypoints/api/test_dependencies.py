from typing import TYPE_CHECKING

from fastapi.security import HTTPAuthorizationCredentials

import pytest

from domain.ports.repositories.crop_repository import CropRepositoryPort

from infrastructure.config import settings
from infrastructure.entrypoints.api.dependencies import (
    get_auth_adapter,
    get_create_crop_use_case,
    get_crop_repository,
    get_get_crop_use_case,
    get_user,
)

if TYPE_CHECKING:
    from faker import Faker
    from pytest_mock import MockerFixture

pytestmark = [
    pytest.mark.unit,
]


def test_get_auth_adapter_not_implemented(
    monkeypatch,
    faker: Faker,
):
    monkeypatch.setattr(settings, 'AUTH_ENGINE', faker.pystr())

    with pytest.raises(NotImplementedError, match=r'No auth adapter for .+'):
        get_auth_adapter()


@pytest.mark.null_auth
def test_get_auth_adapter_null_auth_token_verifier(monkeypatch):
    monkeypatch.setattr(settings, 'AUTH_ENGINE', 'null_auth')

    auth_adapter = get_auth_adapter()

    from infrastructure.adapters.auth.null_auth import NullAuthTokenVerifier

    assert isinstance(auth_adapter, NullAuthTokenVerifier)


@pytest.mark.oauth0
def test_get_auth_adapter_auth0_rs256_token_verifier(monkeypatch):
    monkeypatch.setattr(settings, 'AUTH_ENGINE', 'oauth0')

    auth_adapter = get_auth_adapter()

    from infrastructure.adapters.auth.jwt_asymmetric import (
        Auth0RS256TokenVerifier,
    )

    assert isinstance(auth_adapter, Auth0RS256TokenVerifier)


@pytest.mark.asyncio
async def test_get_user_raises_http_exception_401_on_value_error(
    mocker: MockerFixture,
    faker: Faker,
):
    mocker.patch(
        'infrastructure.entrypoints.api.dependencies.auth_adapter.verify_token',
        side_effect=ValueError('Invalid token signature'),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme='bearer',
        credentials=faker.sha256(),
    )

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await get_user(credentials=credentials)

    from fastapi import status

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Invalid token signature'
    assert exc_info.value.headers == {'WWW-Authenticate': 'Bearer'}


@pytest.mark.asyncio
async def test_get_user_success_ok(
    authenticated_user,
    mocker: MockerFixture,
    faker: Faker,
):
    mocker.patch(
        'infrastructure.entrypoints.api.dependencies.auth_adapter.verify_token',
        return_value=authenticated_user,
    )

    credentials = HTTPAuthorizationCredentials(
        scheme='bearer',
        credentials=faker.sha256(),
    )

    user = await get_user(credentials=credentials)

    assert user == authenticated_user

    from domain.models.auth import AuthenticatedUser

    assert isinstance(user, AuthenticatedUser)


@pytest.mark.asyncio
async def test_get_crop_repository_not_implemented_error(
    monkeypatch,
    faker: Faker,
):
    monkeypatch.setattr(settings, 'DATABASE_ENGINE', faker.pystr())

    with pytest.raises(
        NotImplementedError, match=r'No persistence layer adapter for .+$'
    ):
        await get_crop_repository()


@pytest.mark.in_memory
@pytest.mark.asyncio
async def test_get_crop_repository_in_memory(monkeypatch):
    monkeypatch.setattr(settings, 'DATABASE_ENGINE', 'in_memory')

    from infrastructure.adapters.persistence.in_memory.crop_repository import (
        InMemoryCropRepository,
    )

    repository = await get_crop_repository()

    assert isinstance(repository, InMemoryCropRepository)


@pytest.mark.asyncio
async def test_get_create_crop_use_case_success_ok(mocker: MockerFixture):
    use_case = await get_create_crop_use_case(
        repo=mocker.MagicMock(spec=CropRepositoryPort),
    )

    from application.use_cases.crop.create_crop_use_case import (
        CreateCropUseCase,
    )

    assert isinstance(use_case, CreateCropUseCase)


@pytest.mark.asyncio
async def test_get_get_crop_use_case_success_ok(mocker: MockerFixture):
    use_case = await get_get_crop_use_case(
        repo=mocker.MagicMock(spec=CropRepositoryPort),
    )

    from application.use_cases.crop.get_crop_use_case import (
        GetCropUseCase,
    )

    assert isinstance(use_case, GetCropUseCase)
