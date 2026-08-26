import logging
import uuid
from collections.abc import Iterable

import jwt
from jwt import PyJWKClient

from domain.models.auth import AuthenticatedUser, Permission
from domain.ports.auth.auth_port import TokenVerifierPort
from domain.ports.auth.exceptions import JWTAuthenticationError

logger = logging.getLogger(__name__)


class Auth0RS256TokenVerifier(TokenVerifierPort):
    """
    Implementation of Auth0 Asymmetric key-pair under RS256.
    """

    def __init__(self, domain: str, audience: str):
        self.domain = domain.rstrip('/')
        self.audience = audience
        self.issuer = f'https://{self.domain}/'

        # PyJWKClient handles fetching and caching jwks.json automatically
        jwks_url = f'{self.issuer}.well-known/jwks.json'
        self.jwks_client = PyJWKClient(jwks_url)

    async def verify_token(self, token: str) -> AuthenticatedUser:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                jwt=token,
                key=signing_key,
                algorithms=['RS256'],
                audience=self.audience,
                issuer=self.issuer,
            )

            # We make sure the payload has all the data we need
            if not (
                'sub' in payload and 'email' in payload and 'role' in payload
            ):
                raise JWTAuthenticationError(
                    'Payload malformed. It does not contain the required field.',
                )

            # We make sure the role is an iterable of perms
            if isinstance(payload['role'], str):
                payload['role'] = {payload['role']}
            if not isinstance(payload['role'], Iterable):
                raise TypeError("The property 'role' is not an iterable.")

            return AuthenticatedUser(
                id=uuid.UUID(payload['sub']),
                email=payload['email'],
                permissions={Permission(perm) for perm in payload['role']},
            )
        except (jwt.PyJWTError, TypeError, ValueError) as e:
            raise JWTAuthenticationError(
                'Token validation failed:', str(e)
            ) from e
