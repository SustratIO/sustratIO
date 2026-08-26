from pydantic import BaseModel, Field


class CreateCropRequest(BaseModel):
    """
    Data for crop registration.
    """

    name: str = Field(
        description='The name you can identify the crop by.',
        examples=['Basil'],
    )
    unique_name: str | None = Field(
        default=None,
        description='Either scientific name or any other unique name identifier.',
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
