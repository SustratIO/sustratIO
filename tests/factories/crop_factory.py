import factory

from domain.models.crop import Crop, Fortnight, Month, SowingPeriod


class SowingPeriodFactory(factory.base.Factory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = SowingPeriod

    month = factory.faker.Faker('enum', enum_cls=Month)  # pyright: ignore[reportArgumentType]
    fortnight = factory.faker.Faker('enum', enum_cls=Fortnight)  # pyright: ignore[reportArgumentType]


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
    sowing_season_start = factory.declarations.Maybe(
        decider=factory.faker.Faker('boolean'),
        yes_declaration=factory.declarations.SubFactory(SowingPeriodFactory),  # pyright: ignore[reportArgumentType]
        no_declaration=None,  # pyright: ignore[reportArgumentType]
    )
    sowing_season_end = factory.declarations.Maybe(
        decider=factory.faker.Faker('boolean'),
        yes_declaration=factory.declarations.SubFactory(SowingPeriodFactory),  # pyright: ignore[reportArgumentType]
        no_declaration=None,  # pyright: ignore[reportArgumentType]
    )
    owner_id = factory.faker.Faker('uuid4')
