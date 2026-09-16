import datetime

import factory

from domain.models.crop import Crop


class CropFactory(factory.base.Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Crop

    name = factory.declarations.Sequence(lambda idx: f'Crop {idx:03d}')
    species = factory.declarations.Maybe(
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
    planted_at = factory.faker.Faker('past_datetime', tzinfo=datetime.UTC)
    owner_id = factory.faker.Faker('uuid4')
