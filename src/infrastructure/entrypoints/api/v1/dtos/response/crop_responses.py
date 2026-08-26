from pydantic import BaseModel, Field

from infrastructure.entrypoints.api.v1.dtos.common.mixins.audit import (
    AuditTimestampMixin,
    UniqueIdentifier,
)


class SingleCropResponse(BaseModel, UniqueIdentifier, AuditTimestampMixin):
    """
    Data modeling for a single crop.
    """

    name: str = Field(
        description='The name you can identify the crop by.',
        examples=['Basil'],
    )
    unique_name: str | None = Field(
        description=(
            'Either scientific name or any other unique name identifier.'
        ),
        examples=['Ocimum basilicum'],
    )
    description: str | None = Field(
        description='Description for the crop if needed.',
        examples=[
            'Basil (Ocimum basilicum), also called great basil, is a culinary herb...'
        ],
    )
    notes: str | None = Field(
        description='Any additional notes you might attach to the crop.',
        examples=['Needs water.'],
    )
