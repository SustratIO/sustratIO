"""
Mixin classes that attach audit metadata—such as creation and update
timestamps to models for tracking data provenance and state transitions.
"""

import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class UniqueIdentifier:
    """
    Adds a unique identified based on :class:`uuid.UUID` to the model.

    :param id: The unique identifier.
    :type id: :class:`uuid.UUID`.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(kw_only=True)
class AuditTimestampMixin:
    """
    Adds timestamp fields for tracking creation and transformations.

    :param created_at: Timestamp at which the entry was created.
    :type created_at: :class:`datetime.datetime`
    :param updated_at: Timestamp at which the entry was last updated.
    :type created_at: :class:`datetime.datetime`
    """

    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC,
        ),
    )
    updated_at: datetime.datetime | None = None
