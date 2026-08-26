from typing import TYPE_CHECKING

import pytest

from domain.models.auth import AuthenticatedUser

from infrastructure.adapters.auth.null_auth import NullAuthTokenVerifier

if TYPE_CHECKING:
    from faker import Faker


pytestmark = [
    pytest.mark.unit,
]


@pytest.fixture
def null_auth_verifier(authenticated_user: AuthenticatedUser):
    return NullAuthTokenVerifier(
        identifier=authenticated_user.id,
        email=authenticated_user.email,
        permissions=authenticated_user.permissions,
    )


@pytest.mark.null_auth
@pytest.mark.asyncio
async def test_verify_token_success(
    null_auth_verifier,
    faker: Faker,
):
    user = await null_auth_verifier.verify_token(token=faker.pystr())

    assert isinstance(user, AuthenticatedUser)
