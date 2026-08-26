import uuid

import factory

from domain.models.auth import AuthenticatedUser, Permission


class AuthenticatedUserFactory(factory.base.Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = AuthenticatedUser

    id = factory.declarations.LazyFunction(uuid.uuid4)
    email = factory.faker.Faker('email')
    permissions = factory.declarations.LazyFunction(
        lambda: {perm for perm in Permission},
    )
