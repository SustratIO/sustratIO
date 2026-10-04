from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import uuid

    from domain.models.pagination import CursorPage
    from domain.models.plot import Plot, PlotSearchCriteria


class PlotRepository(Protocol):
    """
    Defines domain logic for interacting with plot entities.
    """

    async def save(
        self,
        plot: Plot,
    ) -> Plot:
        """
        Persists or updates the given :class:`Plot` object in the database.

        :param plot: The plot object to store or update.
        :type plot: :class:`Plot`
        :return: The persisted Plot object (with the relevant permuted data if
                 any).
        :rtype: :class:`Plot`
        """
        ...

    async def find_one(
        self,
        identifier: uuid.UUID,
    ) -> Plot | None:
        """
        Given a unique identifier, returns the associated plot.

        :param identifier: The unique identifier for the plot.
        :type identifier: :class:`uuid.UUID`
        :return: Plot object if found, None otherwise.
        :rtype: :class:`Plot` | None
        """
        ...

    async def find_many_cursor_paginated(
        self,
        filters: PlotSearchCriteria,
        limit: int = 100,
        cursor: str | None = None,
    ) -> CursorPage[Plot]:
        """
        Given the filters, returns a paginated list of plots.

        :param filters: Criteria to filter by.
        :type filters: :class:`PlotSearchCriteria`
        :param limit: Maximum number of plots to return.
        :type limit: int
        :param cursor: Cursor for pagination.
        :type cursor: str | None
        :return: CursorPage containing the paginated list of plots.
        :rtype: CursorPage[Plot]
        """
        ...
