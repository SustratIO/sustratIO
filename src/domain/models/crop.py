"""
The models contained here hold and perform transformations on data regarding
common and specific crops.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from domain.exceptions.validation import StringTooLongError
from domain.models.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifier,
)

if TYPE_CHECKING:
    import uuid


@dataclass(kw_only=True)
class Crop(UniqueIdentifier, AuditTimestampMixin):
    """
    :param name: Name of the crop.
    :type name: str
    :param unique_name: Scientific name or any other unique name identifier.
    :type unique_name: str | None
    :param description: Description of the crop.
    :type description: str | None
    :param notes: Notes associated to this crop.
    :type notes: str | None
    :param owner: The :class:`User` this crops belongs to.
    :type owner: :class:`User`
    """

    name: str
    unique_name: str | None = None
    description: str | None = None
    notes: str | None = None
    owner_id: uuid.UUID

    def __post_init__(self):
        if len(self.name) > 255:
            raise StringTooLongError(
                field_name='name',
                max_length=255,
                current_length=len(self.name),
            )

        if self.unique_name and len(self.unique_name) > 255:
            raise StringTooLongError(
                field_name='unique_name',
                max_length=255,
                current_length=len(self.unique_name),
            )
