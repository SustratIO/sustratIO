from typing import TYPE_CHECKING

import pytest

from domain.models.auth import Permission
from domain.ports.auth.exceptions import JWTAuthenticationError

from infrastructure.adapters.auth.jwt_asymmetric import (
    Auth0RS256TokenVerifier,
)

if TYPE_CHECKING:
    from collections.abc import Generator

    from faker import Faker
    from pytest_mock import MockerFixture

pytestmark = [
    pytest.mark.unit,
]


@pytest.fixture
def oath0_jwt_verifier(
    mocker: MockerFixture,
) -> Generator[Auth0RS256TokenVerifier]:
    """
    Returns an Auth0RS256TokenVerifier with the PyJWKClient mocked out.
    """

    mocker.patch('infrastructure.adapters.auth.jwt_asymmetric.PyJWKClient')

    yield Auth0RS256TokenVerifier(
        domain='example.auth0.com', audience='test-audience'
    )


@pytest.mark.oauth0
@pytest.mark.asyncio
async def test_verify_token_success(
    oath0_jwt_verifier,
    mocker: MockerFixture,
    faker: Faker,
):
    user_id = faker.uuid4(cast_to=None)
    mock_decode = mocker.patch('jwt.decode')
    mock_decode.return_value = {
        'sub': str(user_id),
        'email': 'user@example.com',
        'role': ['read:crop', 'write:crop'],
    }

    authenticated_user = await oath0_jwt_verifier.verify_token(
        'dummy.jwt.token'
    )

    assert authenticated_user.id == user_id
    assert authenticated_user.email == 'user@example.com'
    assert authenticated_user.permissions == {
        Permission.READ_CROP,
        Permission.WRITE_CROP,
    }


@pytest.mark.oauth0
@pytest.mark.asyncio
async def test_verify_token_malformed_payload(
    oath0_jwt_verifier,
    mocker: MockerFixture,
    faker: Faker,
):
    mock_decode = mocker.patch('jwt.decode')
    # Missing 'email' and 'role'
    mock_decode.return_value = {
        'sub': str(faker.uuid4(cast_to=None)),
    }

    with pytest.raises(JWTAuthenticationError, match=r'Payload malformed'):
        await oath0_jwt_verifier.verify_token('dummy.jwt.token')


@pytest.mark.oauth0
@pytest.mark.asyncio
async def test_verify_token_invalid_role_type_not_iterable(
    oath0_jwt_verifier,
    mocker: MockerFixture,
    faker: Faker,
):
    mock_decode = mocker.patch('jwt.decode')
    mock_decode.return_value = {
        'sub': str(faker.uuid4(cast_to=None)),
        'email': 'user@example.com',
        'role': 1,
    }

    with pytest.raises(
        JWTAuthenticationError,
        match="The property 'role' is not an iterable.",
    ):
        await oath0_jwt_verifier.verify_token('dummy.jwt.token')


@pytest.mark.oauth0
@pytest.mark.asyncio
async def test_verify_token_role_type_is_invalid_permission(
    oath0_jwt_verifier,
    mocker: MockerFixture,
    faker: Faker,
):
    mock_decode = mocker.patch('jwt.decode')
    mock_decode.return_value = {
        'sub': str(faker.uuid4(cast_to=None)),
        'email': 'user@example.com',
        'role': 'non-existent permission',
    }

    with pytest.raises(
        JWTAuthenticationError,
        match="'non-existent permission' is not a valid Permission",
    ):
        await oath0_jwt_verifier.verify_token('dummy.jwt.token')


@pytest.mark.oauth0
@pytest.mark.asyncio
async def test_verify_token_jwt_error(oath0_jwt_verifier):
    import jwt

    # Simulate a PyJWT error during decoding or key fetching
    oath0_jwt_verifier.jwks_client.get_signing_key_from_jwt.side_effect = (
        jwt.PyJWTError('Signature verification failed')
    )

    with pytest.raises(
        JWTAuthenticationError, match=r'Token validation failed:'
    ):
        await oath0_jwt_verifier.verify_token('invalid.jwt.token')
