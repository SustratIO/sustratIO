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
