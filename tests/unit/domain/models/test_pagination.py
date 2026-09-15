import base64
import datetime
import json
from typing import TYPE_CHECKING

import pytest

from domain.exceptions.validation import InvalidCursorData
from domain.models.pagination import CursorPage

if TYPE_CHECKING:
    from faker import Faker

pytestmark = [
    pytest.mark.unit,
]


def test_encode_and_decode_cursor_success(faker: Faker):
    id = faker.uuid4(cast_to=str)
    timestamp = faker.date_time(tzinfo=datetime.UTC)

    cursor = CursorPage.encode_cursor(
        cursor_data={
            'id': id,
            'timestamp': timestamp,
        }
    )

    data = CursorPage.decode_cursor(cursor=cursor.decode())

    assert data['id'] == id
    assert data['timestamp'] == timestamp


def test_decode_non_base64_cursor_raises_invalid_cursor_data(faker: Faker):
    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.decode_cursor(cursor=faker.pystr())


def test_decode_non_json_cursor_raises_invalid_cursor_data(faker: Faker):
    cursor = base64.b64encode(faker.text().encode()).decode()

    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.decode_cursor(cursor=cursor)


def test_decode_missing_json_required_properties_raises_invalid_cursor_data():
    cursor = base64.b64encode(json.dumps({}).encode()).decode()

    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.decode_cursor(cursor=cursor)


def test_decode_incorrect_timestamp_format_raises_invalid_cursor_data(
    faker: Faker,
):
    data = {
        'id': faker.uuid4(cast_to=str),
        'timestamp': faker.date_time(
            tzinfo=datetime.UTC,
        ).strftime(
            format='%d/%m/%Y, %H:%M:%S',
        ),
    }
    cursor = base64.b64encode(json.dumps(data).encode()).decode()

    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.decode_cursor(cursor=cursor)


def test_encode_incorrect_timestamp_format_raises_invalid_cursor_data(
    faker: Faker,
):
    cursor_data = {
        'id': faker.uuid4(cast_to=str),
        'timestamp': faker.pystr(),
    }

    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.encode_cursor(cursor_data=cursor_data)  # pyright: ignore[reportArgumentType]


def test_encode_missing_json_required_properties_raises_invalid_cursor_data():
    with pytest.raises(InvalidCursorData, match='Invalid cursor data: '):
        CursorPage.encode_cursor(cursor_data={})  # pyright: ignore[reportArgumentType]
