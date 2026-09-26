import logging
from typing import TYPE_CHECKING, Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.models.auth import AuthenticatedUser, Permission
from domain.ports.repositories.crop_repository import CropRepositoryPort

from application.use_cases.crop.create_crop_use_case import CreateCropUseCase
from application.use_cases.crop.get_crop_use_case import GetCropUseCase
from application.use_cases.crop.list_crops_use_case import ListCropsUseCase
from application.use_cases.crop.update_crop_use_case import UpdateCropUseCase

from infrastructure.config import settings

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from domain.ports.auth.token_auth_port import TokenVerifierPort


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


GetUserDeps = Annotated[
    AuthenticatedUser,
    Depends(get_user),
]


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


def require_permissions(
    *permissions: Permission,
    require_all: bool = False,
) -> Callable[[GetUserDeps], Coroutine[Any, Any, AuthenticatedUser]]:
    """
    Factory returning a dependency function that verifies user permissions.

    :param permissions: The permissions to check.
    :param require_all: If True, the user must have all specified permissions.
                        If False, the user must have at least one of the
                        specified permissions.
    :return: A coroutine function that checks the user's permissions and
             returns the user if authorized.
    :rtype: Callable[[GetUserDeps], Coroutine[Any, Any, AuthenticatedUser]]
    """

    async def _check_permissions(user: GetUserDeps) -> AuthenticatedUser:
        check = user.has_all if require_all else user.has_any

        if not check(*permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions to perform this action.',
            )

        return user

    return _check_permissions


RequireReadCropsDeps = Annotated[
    AuthenticatedUser,
    Depends(require_permissions(Permission.READ_CROPS)),
]

RequireWriteCropsDeps = Annotated[
    AuthenticatedUser,
    Depends(require_permissions(Permission.WRITE_CROPS)),
]

RequireReadAndWriteCropsDeps = Annotated[
    AuthenticatedUser,
    Depends(
        require_permissions(
            Permission.READ_CROPS,
            Permission.WRITE_CROPS,
            require_all=True,
        )
    ),
]


async def get_create_crop_use_case(repo: CropRepoDeps) -> CreateCropUseCase:
    """
    Dependency injection for crop creation use case.

    :return: The use case instance.
    :rtype: :class:`CreateCropUseCase`
    """

    use_case = CreateCropUseCase(repo=repo)
    return use_case


CreateCropUseCaseDeps = Annotated[
    CreateCropUseCase,
    Depends(get_create_crop_use_case),
]


async def get_get_crop_use_case(repo: CropRepoDeps) -> GetCropUseCase:
    """
    Dependency injection for crop retrieval by ID use case.

    :return: The use case instance.
    :rtype: :class:`GetCropUseCase`
    """

    use_case = GetCropUseCase(repo=repo)
    return use_case


GetCropUseCaseDeps = Annotated[
    GetCropUseCase,
    Depends(get_get_crop_use_case),
]


async def get_update_crop_use_case(repo: CropRepoDeps) -> UpdateCropUseCase:
    """
    Dependency injection for crop update use case.

    :return: The use case instance.
    :rtype: :class:`UpdateCropUseCase`
    """

    use_case = UpdateCropUseCase(repo=repo)
    return use_case


UpdateCropUseCaseDeps = Annotated[
    UpdateCropUseCase,
    Depends(get_update_crop_use_case),
]


async def get_list_crops_use_case(repo: CropRepoDeps) -> ListCropsUseCase:
    """
    Dependency injection for listing crops use case.

    :return: The use case instance.
    :rtype: :class:`ListCropsUseCase`
    """

    use_case = ListCropsUseCase(repo=repo)
    return use_case


ListCropsUseCaseDeps = Annotated[
    ListCropsUseCase,
    Depends(get_list_crops_use_case),
]
