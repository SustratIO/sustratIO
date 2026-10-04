import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query, status

from domain.models.crop import (
    CropSearchCriteria,
    Fortnight,
    Month,
    SowingPeriod,
)

from application.dtos.crop_dtos import (
    CreateCropInput,
    UpdateCropInput,
)

from infrastructure.entrypoints.api.dependencies import (
    CreateCropUseCaseDeps,
    GetCropUseCaseDeps,
    ListCropsUseCaseDeps,
    RequireReadAndWriteCropsDeps,
    RequireReadCropsDeps,
    RequireWriteCropsDeps,
    UpdateCropUseCaseDeps,
)
from infrastructure.entrypoints.api.v1.dtos.common.crop import SowingPeriodDTO
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

    sowing_season_start = None
    if data.sowing_season_start:
        sowing_season_start = SowingPeriod(
            month=Month(data.sowing_season_start.month),
            fortnight=Fortnight(data.sowing_season_start.fortnight),
        )

    sowing_season_end = None
    if data.sowing_season_end:
        sowing_season_end = SowingPeriod(
            month=Month(data.sowing_season_end.month),
            fortnight=Fortnight(data.sowing_season_end.fortnight),
        )

    input_data = CreateCropInput(
        name=data.name,
        species=data.species,
        description=data.description,
        notes=data.notes,
        sowing_season_start=sowing_season_start,
        sowing_season_end=sowing_season_end,
    )

    crop = await use_case.execute(
        input_data=input_data,
        user=user,
    )

    crop_sowing_season_start: SowingPeriodDTO | None = None
    if crop.sowing_season_start:
        crop_sowing_season_start = SowingPeriodDTO(
            month=crop.sowing_season_start.month,
            fortnight=crop.sowing_season_start.fortnight,
        )

    crop_sowing_season_end: SowingPeriodDTO | None = None
    if crop.sowing_season_end:
        crop_sowing_season_end = SowingPeriodDTO(
            month=crop.sowing_season_end.month,
            fortnight=crop.sowing_season_end.fortnight,
        )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
        description=crop.description,
        notes=crop.notes,
        sowing_season_start=crop_sowing_season_start,
        sowing_season_end=crop_sowing_season_end,
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

    crop_sowing_season_start: SowingPeriodDTO | None = None
    if crop.sowing_season_start:
        crop_sowing_season_start = SowingPeriodDTO(
            month=crop.sowing_season_start.month,
            fortnight=crop.sowing_season_start.fortnight,
        )

    crop_sowing_season_end: SowingPeriodDTO | None = None
    if crop.sowing_season_end:
        crop_sowing_season_end = SowingPeriodDTO(
            month=crop.sowing_season_end.month,
            fortnight=crop.sowing_season_end.fortnight,
        )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
        description=crop.description,
        notes=crop.notes,
        sowing_season_start=crop_sowing_season_start,
        sowing_season_end=crop_sowing_season_end,
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

    sowing_season_start: SowingPeriod | None = None
    if data.sowing_season_start:
        sowing_season_start = SowingPeriod(
            month=Month(data.sowing_season_start.month),
            fortnight=Fortnight(data.sowing_season_start.fortnight),
        )

    sowing_season_end: SowingPeriod | None = None
    if data.sowing_season_end:
        sowing_season_end = SowingPeriod(
            month=Month(data.sowing_season_end.month),
            fortnight=Fortnight(data.sowing_season_end.fortnight),
        )

    input_data = UpdateCropInput(
        name=data.name,
        species=data.species,
        description=data.description,
        notes=data.notes,
        sowing_season_start=sowing_season_start,
        sowing_season_end=sowing_season_end,
    )

    crop = await use_case.execute(
        identifier=identifier,
        input_data=input_data,
        user=user,
    )

    crop_sowing_season_start: SowingPeriodDTO | None = None
    if crop.sowing_season_start:
        crop_sowing_season_start = SowingPeriodDTO(
            month=crop.sowing_season_start.month,
            fortnight=crop.sowing_season_start.fortnight,
        )

    crop_sowing_season_end: SowingPeriodDTO | None = None
    if crop.sowing_season_end:
        crop_sowing_season_end = SowingPeriodDTO(
            month=crop.sowing_season_end.month,
            fortnight=crop.sowing_season_end.fortnight,
        )

    return SingleCropResponse(
        id=crop.id,
        name=crop.name,
        species=crop.species,
        description=crop.description,
        notes=crop.notes,
        sowing_season_start=crop_sowing_season_start,
        sowing_season_end=crop_sowing_season_end,
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

    crops_responses = []
    for crop in paginated_crops.items:
        crop_sowing_season_start: SowingPeriodDTO | None = None
        if crop.sowing_season_start:
            crop_sowing_season_start = SowingPeriodDTO(
                month=crop.sowing_season_start.month,
                fortnight=crop.sowing_season_start.fortnight,
            )

        crop_sowing_season_end: SowingPeriodDTO | None = None
        if crop.sowing_season_end:
            crop_sowing_season_end = SowingPeriodDTO(
                month=crop.sowing_season_end.month,
                fortnight=crop.sowing_season_end.fortnight,
            )

        crops_responses.append(
            SingleCropResponse(
                id=crop.id,
                name=crop.name,
                species=crop.species,
                description=crop.description,
                notes=crop.notes,
                sowing_season_start=crop_sowing_season_start,
                sowing_season_end=crop_sowing_season_end,
                created_at=crop.created_at,
                updated_at=crop.updated_at,
            )
        )

    return CursorPaginationResponse(
        items=crops_responses,
        next_cursor=paginated_crops.next_cursor,
    )
