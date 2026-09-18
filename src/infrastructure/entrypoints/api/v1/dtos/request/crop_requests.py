import datetime

from pydantic import BaseModel, Field


class CreateCropRequest(BaseModel):
    """
    Data for crop registration.
    """

    name: str = Field(
        description='Common crop name.',
        examples=['Basil'],
    )
    species: str | None = Field(
        default=None,
        description='Botanical species name.',
        examples=['Ocimum basilicum'],
    )
    description: str | None = Field(
        default=None,
        description='Description for the crop if needed.',
        examples=[
            'Basil (Ocimum basilicum), also called great basil, is a culinary herb...'
        ],
    )
    notes: str | None = Field(
        default=None,
        description='Any additional notes you might attach to the crop.',
        examples=['Needs water.'],
    )
    planted_at: datetime.datetime = Field(
        description='Timestamp when planted.',
    )


class UpdateCropRequest(BaseModel):
    """
    Data for updating a crop.
    """

    name: str | None = Field(
        default=None,
        description='Common crop name.',
        examples=['Basil'],
    )
    species: str | None = Field(
        default=None,
        description='Botanical species name.',
        examples=['Ocimum basilicum'],
    )
    description: str | None = Field(
        default=None,
        description='Description for the crop if needed.',
        examples=[
            'Basil (Ocimum basilicum), also called great basil, is a culinary herb...'
        ],
    )
    notes: str | None = Field(
        default=None,
        description='Any additional notes you might attach to the crop.',
        examples=['Needs water.'],
    )
    planted_at: datetime.datetime | None = Field(
        default=None,
        description='Timestamp when planted.',
    )


class CropSearchQueryParams(BaseModel):
    """
    Model for filtering a list of crops.
    """

    limit: int = Field(
        default=100,
        description='Number of entries to return.',
    )
    cursor: str | None = Field(
        default=None,
        description='Cursor from where to start the next set.',
    )
    name: str | None = Field(
        default=None,
        description='Common crop name. Case insensitive.',
    )
    species: str | None = Field(
        default=None,
        description='Botanical species name. Case insensitive.',
    )
    description: str | None = Field(
        default=None,
        description='Description of the crop. Case insensitive.',
    )
    notes: str | None = Field(
        default=None,
        description='Notes associated to this crop. Case insensitive.',
    )
    planted_at: datetime.datetime | None = Field(
        default=None,
        description=(
            'Timestamp when planted. It searches within 12 hours of this.'
        ),
    )
