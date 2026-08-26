"""
Contains the launcher creation logic for the API integration.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Handles the logic at runtime for the app entrypoint creation.
    """

    # Log configuration
    from infrastructure.config import settings
    from infrastructure.logging_config import setup_logging

    setup_logging(log_level=settings.log_level)

    from fastapi import FastAPI

    tags = [
        {
            'name': 'crops',
            'description': 'Operation with crops.',
        }
    ]
    app = FastAPI(
        title='SustratIO API',
        description='Design to monitor, notify and track soil quality.',
        version='0.0.1',
        openapi_tags=tags,
    )

    # Version routers
    from infrastructure.entrypoints.api.v1.router import router_v1

    app.include_router(router_v1)

    # Exception handlers
    from domain.exceptions.auth import PermissionDeniedException
    from domain.exceptions.repository import EntityNotFoundException

    from infrastructure.entrypoints.api.exception_handlers import (
        not_found_exception_handler,
        permission_denied_exception_handler,
    )

    app.add_exception_handler(
        PermissionDeniedException,
        permission_denied_exception_handler,
    )
    app.add_exception_handler(
        EntityNotFoundException,
        not_found_exception_handler,
    )

    return app
