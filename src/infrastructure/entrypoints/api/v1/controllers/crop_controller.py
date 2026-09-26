import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query, status

from domain.models.crop import CropSearchCriteria

from application.dtos.crop_dtos import CreateCropInput, UpdateCropInput

from infrastructure.entrypoints.api.dependencies import (
    CreateCropUseCaseDeps,
    GetCropUseCaseDeps,
    ListCropsUseCaseDeps,
    RequireReadAndWriteCropsDeps,
    RequireReadCropsDeps,
    RequireWriteCropsDeps,
    UpdateCropUseCaseDeps,
)
from infrastructure.entrypoints.api.v1.dtos.request.crop_requests import (
    CreateCropRequest,
    CropSearchQueryParams,
    UpdateCropRequest,
)
from infrastructure.entrypoints.api.v1.dtos.response.crop_responses import (
    SingleCropResponse,
)
from infrastructure.entrypoints.api.v1.dtos.response.pagination_responses import (
    CursorPaginationResponse,
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
    user: RequireWriteCropsDeps,
):
    """
    Creates a single crop with the given data.
    """

    input_data = CreateCropInput(
        name=data.name,
        species=data.species,
        description=data.description,
        notes=data.notes,
    )

    crop = await use_case.execute(
        input_data=input_data,
        user=user,
    )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
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
    identifier: Annotated[
        uuid.UUID,
        Path(description='Unique identifier for the crop.'),
    ],
    use_case: GetCropUseCaseDeps,
    user: RequireReadCropsDeps,
):
    """
    Given an ID it returns a crop if it exists.
    """

    crop = await use_case.execute(
        identifier=identifier,
        user=user,
    )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
        description=crop.description,
        notes=crop.notes,
        created_at=crop.created_at,
        updated_at=crop.updated_at,
    )


@crops_router.put(
    '/{identifier}',
    summary='Updates the given ID crop.',
    response_model=SingleCropResponse,
    status_code=status.HTTP_200_OK,
)
async def update_crop(
    identifier: Annotated[
        uuid.UUID,
        Path(description='Unique identifier for the crop.'),
    ],
    data: Annotated[
        UpdateCropRequest,
        Body(description='Data for the crop update.'),
    ],
    use_case: UpdateCropUseCaseDeps,
    user: RequireReadAndWriteCropsDeps,
):
    """
    Given an ID, it updates a crop with the given data in body.
    """

    input_data = UpdateCropInput(
        name=data.name,
        species=data.species,
        description=data.description,
        notes=data.notes,
    )

    crop = await use_case.execute(
        identifier=identifier,
        input_data=input_data,
        user=user,
    )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
        description=crop.description,
        notes=crop.notes,
        created_at=crop.created_at,
        updated_at=crop.updated_at,
    )


@crops_router.get(
    '/',
    summary='Returns a paginated set of crops.',
    response_model=CursorPaginationResponse[SingleCropResponse],
    status_code=status.HTTP_200_OK,
)
async def list_crops(
    query: Annotated[
        CropSearchQueryParams,
        Query(
            description=(
                'Data for querying and declaring number of entries to return'
            )
        ),
    ],
    use_case: ListCropsUseCaseDeps,
    user: RequireReadCropsDeps,
):
    criteria = CropSearchCriteria(
        name=query.name,
        species=query.species,
        description=query.description,
        notes=query.notes,
        owner_id=user.id,
    )

    paginated_crops = await use_case.execute(
        criteria=criteria,
        limit=query.limit,
        user=user,
        cursor=query.cursor,
    )

    return CursorPaginationResponse(
        items=paginated_crops.items,
        next_cursor=paginated_crops.next_cursor,
    )
