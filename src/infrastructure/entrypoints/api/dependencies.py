import logging
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.models.auth import AuthenticatedUser
from domain.ports.repositories.crop_repository import CropRepositoryPort

from application.use_cases.crop.create_crop_use_case import CreateCropUseCase
from application.use_cases.crop.get_crop_use_case import GetCropUseCase

from infrastructure.config import settings

if TYPE_CHECKING:
    from domain.ports.auth.auth_port import TokenVerifierPort


logger = logging.getLogger(__name__)


def get_auth_adapter() -> TokenVerifierPort:
    """
    Given the configuration, it returns the authentication method.

    :return: The port for the authentication layer.
    :rtype: :class:`TokenVerifierPort`
    """

    if settings.AUTH_ENGINE == 'null_auth':
        from infrastructure.adapters.auth.null_auth import (
            NullAuthTokenVerifier,
        )

        return NullAuthTokenVerifier()

    if settings.AUTH_ENGINE == 'oauth0':
        from infrastructure.adapters.auth.jwt_asymmetric import (
            Auth0RS256TokenVerifier,
        )

        return Auth0RS256TokenVerifier(
            domain=settings.oauth0.domain,
            audience=settings.oauth0.audience,
        )

    raise NotImplementedError(f'No auth adapter for {settings.AUTH_ENGINE}')


auth_adapter = get_auth_adapter()


async def get_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(HTTPBearer())
    ],
) -> AuthenticatedUser:
    """
    Dependency injection for asymmetric token for authorization.

    :return: Authorized user.
    :rtype: :class:`AuthenticatedUser`
    """

    try:
        token = credentials.credentials
        user = await auth_adapter.verify_token(token=token)

        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={'WWW-Authenticate': 'Bearer'},
        )


GetUserDeps = Annotated[AuthenticatedUser, Depends(get_user)]


async def get_crop_repository() -> CropRepositoryPort:
    """
    Dependency injection for crop repository.

    :return: The repository instance.
    :rtype: :class:`CropRepositoryPort`
    """

    if settings.DATABASE_ENGINE == 'in_memory':
        from infrastructure.adapters.persistence.in_memory.crop_repository import (
            InMemoryCropRepository,
        )

        return InMemoryCropRepository()

    raise NotImplementedError(
        f'No persistence layer adapter for {settings.DATABASE_ENGINE}'
    )


CropRepoDeps = Annotated[CropRepositoryPort, Depends(get_crop_repository)]


async def get_create_crop_use_case(repo: CropRepoDeps) -> CreateCropUseCase:
    """
    Dependency injection for crop creation use case.

    :return: The use case instance.
    :rtype: :class:`CreateCropUseCase`
    """

    use_case = CreateCropUseCase(repo=repo)
    return use_case


CreateCropUseCaseDeps = Annotated[
    CreateCropUseCase, Depends(get_create_crop_use_case)
]


async def get_get_crop_use_case(repo: CropRepoDeps) -> GetCropUseCase:
    """
    Dependency injection for crop retrieval by ID use case.

    :return: The use case instance.
    :rtype: :class:`GetCropUseCase`
    """

    use_case = GetCropUseCase(repo=repo)
    return use_case


GetCropUseCaseDeps = Annotated[GetCropUseCase, Depends(get_get_crop_use_case)]
