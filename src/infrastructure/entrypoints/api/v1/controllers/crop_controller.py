import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Body, status

from infrastructure.entrypoints.api.dependencies import (
    CreateCropUseCaseDeps,
    GetCropUseCaseDeps,
    GetUserDeps,
)
from infrastructure.entrypoints.api.v1.dtos.request.crop_requests import (
    CreateCropRequest,
)
from infrastructure.entrypoints.api.v1.dtos.response.crop_responses import (
    SingleCropResponse,
)

logger = logging.getLogger(__name__)

crops_router = APIRouter(prefix='/crops', tags=['crops'])


@crops_router.post(
    '/',
    summary='Creates a single crop',
    response_model=SingleCropResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crop(
    data: Annotated[
        CreateCropRequest,
        Body(description='Data for the crop creation.'),
    ],
    use_case: CreateCropUseCaseDeps,
    user: GetUserDeps,
):
    """
    Creates a single crop with the given data.
    """

    crop = await use_case.execute(
        name=data.name,
        unique_name=data.unique_name,
        description=data.description,
        notes=data.notes,
        user=user,
    )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        unique_name=crop.unique_name,
        description=crop.description,
        notes=crop.notes,
        created_at=crop.created_at,
        updated_at=crop.updated_at,
    )


@crops_router.get(
    '/{identifier}',
    summary='Retrieves a single crop by ID',
    response_model=SingleCropResponse,
    status_code=status.HTTP_200_OK,
)
async def get_crop_by_id(
    identifier: uuid.UUID,
    use_case: GetCropUseCaseDeps,
    user: GetUserDeps,
):
    """
    Given an ID it returns a crop if it exists.
    """

    crop = await use_case.execute(identifier=identifier, user=user)

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        unique_name=crop.unique_name,
        description=crop.description,
        notes=crop.notes,
        created_at=crop.created_at,
        updated_at=crop.updated_at,
    )
