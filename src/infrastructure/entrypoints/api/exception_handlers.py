import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def permission_denied_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Returns 403 Forbidden when a user tries to perform an action that raises
    :class:`domain.exceptions.PermissionDeniedException`.
    """

    logger.error('Permission denied when trying to perform an action: %s', exc)

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': str(exc)},
    )


async def not_found_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Returns 404 Not Found when a user tries to perform an action that raises
    :class:`domain.exceptions.NotFoundException`.
    """

    logger.error('Data not found when trying to perform an action: %s', exc)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': str(exc)},
    )
