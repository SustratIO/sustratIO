from fastapi import APIRouter

from infrastructure.entrypoints.api.v1.controllers.crop_controller import (
    crops_router,
)

router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(crops_router)
