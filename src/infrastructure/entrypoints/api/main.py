#!/usr/env/bin python3

import logging

import uvicorn

from infrastructure.config import settings
from infrastructure.entrypoints.api.app import create_app

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'infrastructure.entrypoints.api.main:app',
        host=str(settings.uvicorn.host.network_address),
        port=settings.uvicorn.port,
        reload=settings.uvicorn.reload,
        workers=settings.uvicorn.workers,
        log_level=settings.log_level,
        use_colors=settings.uvicorn.use_colors,
    )
