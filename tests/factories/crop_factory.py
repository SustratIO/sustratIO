import uuid

import factory

from domain.models.crop import Crop


class CropFactory(factory.base.Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Crop

    name = factory.faker.Faker('name')
    unique_name = factory.declarations.Maybe(
        decider=factory.faker.Faker('boolean'),
        yes_declaration=factory.faker.Faker('name'),  # pyright: ignore[reportArgumentType]
        no_declaration=None,  # pyright: ignore[reportArgumentType]
    )
    description = factory.declarations.Maybe(
        decider=factory.faker.Faker('boolean'),
        yes_declaration=factory.faker.Faker('sentence'),  # pyright: ignore[reportArgumentType]
        no_declaration=None,  # pyright: ignore[reportArgumentType]
    )
    notes = factory.declarations.Maybe(
        decider=factory.faker.Faker('boolean'),
        yes_declaration=factory.faker.Faker('sentence'),  # pyright: ignore[reportArgumentType]
        no_declaration=None,  # pyright: ignore[reportArgumentType]
    )
    owner_id = factory.declarations.LazyFunction(uuid.uuid4)
