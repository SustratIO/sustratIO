from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import uuid

    from domain.models.crop import Crop


class Database(TypedDict):
    crops: dict[uuid.UUID, Crop]


DATABASE: Database = {
    'crops': {},
}
