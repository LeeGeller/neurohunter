"""Vacancy requirements schema."""
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.schemas.knowledge.concept_extraction import (
    ConceptGroupSchema,
    ConceptSchema,
)


class VacancyRequirementsSchema(BaseModel):
    """Schema for vacancy requirements extracted from LLM."""

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
    )

    mandatory_skills: list[ConceptSchema] = Field(
        default_factory=list,
        alias='mandatorySkills',
    )
    mandatory_skill_groups: list[ConceptGroupSchema] = Field(
        default_factory=list,
        alias='mandatorySkillGroups',
    )

    preferred_skills: list[ConceptSchema] = Field(
        default_factory=list,
        alias='preferredSkills',
    )
    preferred_skill_groups: list[ConceptGroupSchema] = Field(
        default_factory=list,
        alias='preferredSkillGroups',
    )

    experience_min: Optional[float] = Field(
        default=None,
        alias='experienceMin',
    )
    experience_max: Optional[float] = Field(
        default=None,
        alias='experienceMax',
    )
    education_requirement: Optional[str] = Field(
        default=None,
        alias='educationRequirement',
    )
    evidence: Optional[list[str]] = Field(
        default=None,
        alias='evidence',
    )
