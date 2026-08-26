import logging
import uuid

from domain.models.auth import AuthenticatedUser, Permission
from domain.ports.auth.auth_port import TokenVerifierPort

logger = logging.getLogger(__name__)


class NullAuthTokenVerifier(TokenVerifierPort):
    """
    Returns a dummy user ignoring the authentication. This is meant to be used
    in development environments.
    """

    identifier: uuid.UUID = uuid.uuid4()

    def __init__(
        self,
        identifier: uuid.UUID | None = None,
        email: str = 'test@sustratio.com',
        permissions: set[Permission] | None = None,
    ) -> None:
        """
        :param identifier: Unique identifier for the user.
                           If not given it uses a static one.
        :type identifier: :class:`uuid.UUID`
        :param email: Email associated to the user.
        :type email: str
        :param permissions: Set of permissions the user have. If not give it
                            automatically has them all.
        :type permissions: set[:class:`Permission`]
        """

        self.identifier = identifier or self.identifier
        self.email = email
        self.permissions = (
            permissions
            if permissions is not None
            else {perm for perm in Permission}
        )

    async def verify_token(self, token: str) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=self.identifier,
            email=self.email,
            permissions=self.permissions,
        )
