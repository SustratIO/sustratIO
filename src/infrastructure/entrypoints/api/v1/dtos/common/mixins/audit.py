import uuid

from pydantic import UUID4, AwareDatetime, Field
from pydantic.dataclasses import dataclass


@dataclass
class UniqueIdentifier:
    """
    Unique identified based on :class:`uuid.UUID` to the model.
    """

    id: UUID4 = Field(
        description='Unique identifier for the entry.',
        # NOTE: this is only to create random examples
        examples=[str(uuid.uuid4()) for _ in range(3)],
    )


@dataclass
class AuditTimestampMixin:
    """
    Timestamp fields for tracking creation and transformations.
    """

    created_at: AwareDatetime = Field(
        description='Timestamp at which the entry was created.',
        examples=['2026-09-01 08:00:00.000000+00:00'],
    )
    updated_at: AwareDatetime | None = Field(
        description='Timestamp at which the entry was last updated.',
        examples=[None, '2026-09-01 08:00:00.000000+00:00'],
    )
