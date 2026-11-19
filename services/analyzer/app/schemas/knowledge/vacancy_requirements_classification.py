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

    mandatory_skills: list[str] = Field(
        default_factory=list,
    )
    preferred_skills: list[str] = Field(
        default_factory=list,
    )
