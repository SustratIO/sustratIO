from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class CursorPaginationResponse[T](BaseModel):
    """
    It returns a paginated set of entries with a cursor pointing to next set if
    any.
    """

    items: list[T] = Field(
        default_factory=list, description='Returned set of entries.'
    )
    next_cursor: str | None = Field(
        default=None, description='Cursor pointing to the next set of entries.'
    )
