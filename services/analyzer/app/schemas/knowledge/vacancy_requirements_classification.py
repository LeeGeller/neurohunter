"""Schema for vacancy requirement classification."""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class VacancyRequirementsClassificationSchema(BaseModel):
    """Classify source text into requirement categories."""

    model_config = ConfigDict(
        extra='forbid',
    )

    mandatory_text: list[str] = Field(
        default_factory=list,
    )
    preferred_text: list[str] = Field(
        default_factory=list,
    )
