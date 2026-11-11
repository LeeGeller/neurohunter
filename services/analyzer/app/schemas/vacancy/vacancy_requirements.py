"""Vacancy requirements schema."""
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class VacancyRequirementsSchema(BaseModel):
    """Schema for vacancy requirements extracted from LLM."""

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
    )

    mandatory_skills: Optional[list[str]] = Field(
        alias='mandatorySkills',
    )
    preferred_skills: Optional[list[str]] = Field(
        alias='preferredSkills',
    )

    experience_min: Optional[float] = Field(
        alias='experienceMin',
    )
    experience_max: Optional[float] = Field(
        alias='experienceMax',
    )
    education_requirement: Optional[str] = Field(
        alias='educationRequirement',
    )
    evidence: Optional[list[str]] = Field(
        default=None,
        alias='evidence',
    )
