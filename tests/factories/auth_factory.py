import factory

from domain.models.auth import AuthenticatedUser, Permission


class AuthenticatedUserFactory(factory.base.Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = AuthenticatedUser

    id = factory.faker.Faker('uuid4')
    email = factory.faker.Faker('email')
    permissions = factory.declarations.LazyFunction(
        lambda: {
            perm
            for perm in Permission
            if perm
            not in {
                Permission.READ_ALL,
                Permission.WRITE_ALL,
                Permission.DELETE_ALL,
            }
        },
    )
