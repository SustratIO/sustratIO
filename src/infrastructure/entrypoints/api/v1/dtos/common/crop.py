from pydantic import BaseModel, Field


class SowingPeriodDTO(BaseModel):
    """
    Data for handling sowing periods. This is not meant to be used alone as a
    request.
    """

    month: int = Field(
        description='Months from 1 to 12 for this sowing season.',
        examples=[n for n in range(1, 12)],
        ge=1,
        le=12,
    )
    fortnight: int = Field(
        description=(
            'Whether the first or second fortnight within given month.'
        ),
        examples=[1, 2],
        ge=1,
        le=2,
    )
