"""Resume features schemas."""
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)


class ProjectSchema(BaseModel):
    """ProjectSchema."""
    name: str
    description: str


class ResumeExperienceSchema(BaseModel):
    """ResumeExperienceSchema."""
    job_title: Optional[str]
    company: Optional[str]
    period: Optional[str]
    description: Optional[str]


class ResumeFeaturesSchema(BaseModel):
    """ResumeFeaturesSchema."""
    job_titles: list[str] = Field(
        default_factory=list,
    )
    hard_skills: list[str] = Field(
        default_factory=list,
    )
    soft_skills: list[str] = Field(
        default_factory=list,
    )

    experience: Optional[float]

    projects: list[ProjectSchema] = Field(
        default_factory=list,
    )
    weaknesses: list[str] = Field(
        default_factory=list,
    )
    strengths: list[str] = Field(
        default_factory=list,
    )

    experience_resume: list[ResumeExperienceSchema] = Field(
        default_factory=list,
    )
