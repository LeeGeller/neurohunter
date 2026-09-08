"""Portfolio features schemas."""
import uuid

from pydantic import (
    BaseModel,
    Field,
)


class ResumeFeatures(BaseModel):
    """Resume features extracted for LLM."""

    user_id: uuid.UUID

    # Parameters used for vacancy matching
    job_titles: list[str] = Field(
        default_factory=list,
    )
    hard_skills: list[str] = Field(
        default_factory=list,
    )
    soft_skills: list[str] = Field(
        default_factory=list,
    )

    experience: float | None = None

    projects: list[str] = Field(
        default_factory=list,
    )

    weaknesses: list[str] = Field(
        default_factory=list,
    )
    strengths: list[str] = Field(
        default_factory=list,
    )

    experience_resume: list[str] = Field(
        default_factory=list,
    )
