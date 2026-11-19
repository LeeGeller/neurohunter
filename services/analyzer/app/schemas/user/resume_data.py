"""Schema for resume data extraction."""

from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.user.resume_features import (
    ProjectSchema,
    ResumeExperienceSchema,
)


class ResumeDataSchema(BaseModel):
    """Extract general information from a resume."""

    job_titles: list[str] = Field(
        default_factory=list,
    )
    hard_skills: list[str] = Field(
        default_factory=list,
    )
    soft_skills: list[str] = Field(
        default_factory=list,
    )
    experience: Optional[float] = None
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
