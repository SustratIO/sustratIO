import base64
import datetime
import json
from dataclasses import dataclass, field
from typing import TypedDict, TypeVar

from domain.exceptions.validation import InvalidCursorData

T = TypeVar('T')


class CursorData(TypedDict):
    """
    Embodies entry data to generate a cursor to the same entry.

    :param id: The unique identifier of the entry.
    :type id: str
    :param timestamp: Timestamp used for referencing this entry
                      (usually `created_at`).
    :type timestamp: :class:`datetime.datetime`
    """

    id: str
    timestamp: datetime.datetime


@dataclass
class CursorPage[T]:
    """
    Returns a list of items :class:`T` and the cursor pointer for the next
    batch.

    In order to generate the cursor you need to provide an identifier and a
    timestamp that meet :class:`CursorData` types. The entries must be first
    ordered using these two parameters.

    :param items: List of items within this page.
    :type items: list[:class:`T`]
    :param cursor: Cursor pointer to next batch.
    :type cursor: str
    """

    items: list[T] = field(default_factory=list)
    cursor: str | None = None

    @staticmethod
    def decode_cursor(cursor: str) -> CursorData:
        """
        Given a cursor it decodes it and returns the encoded fields within a
        dict.

        :param cursor: The cursor in base64.
        :type cursor: str
        :return: `id` and `timestamp` data.
        :rtype: :class:`DecodedData`
        """

        try:
            data = json.loads(base64.b64decode(cursor).decode())
            timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            return {
                'id': data['id'],
                'timestamp': timestamp,
            }
        except (
            ValueError,
            KeyError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as exc:
            raise InvalidCursorData(f'Invalid cursor data: {exc!s}') from exc

    @staticmethod
    def encode_cursor(cursor_data: CursorData) -> bytes:
        """
        Given a dictionary with cursor data it returns the encoded cursor.

        :param cursor_data: Identifier and timestamp for cursor generation.
        :type cursor_data: :class:`CursorData`
        :return: Encoded cursor.
        :rtype: bytes
        """

        try:
            timestamp = cursor_data['timestamp'].isoformat()
            cursor = base64.b64encode(
                json.dumps(
                    {
                        'id': cursor_data['id'],
                        'timestamp': timestamp,
                    }
                ).encode()
            )

            return cursor
        except (
            AttributeError,
            ValueError,
            KeyError,
            UnicodeEncodeError,
        ) as exc:
            raise InvalidCursorData(f'Invalid cursor data: {exc!s}') from exc
