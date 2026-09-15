import datetime
from typing import TYPE_CHECKING

import pytest

from domain.exceptions.validation import ValidationError
from domain.models.common.mixins.audit import AuditTimestampMixin

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


def test_audit_timestamp_mixin_updated_at_before_created_at(faker: Faker):
    created_at = faker.date_time(tzinfo=datetime.UTC)
    updated_at = created_at - datetime.timedelta(days=1)

    with pytest.raises(
        ValidationError, match="Invalid 'updated_at' set before 'created_at' "
    ):
        AuditTimestampMixin(created_at=created_at, updated_at=updated_at)


def test_audit_timestamp_required_data_success(faker: Faker):
    audit = AuditTimestampMixin(
        created_at=faker.date_time(tzinfo=datetime.UTC),
    )

    assert audit is not None
