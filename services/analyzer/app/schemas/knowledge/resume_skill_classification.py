"""Schema for resume skill classification."""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ResumeSkillClassificationSchema(BaseModel):
    """Classify resume text into skill categories."""

    model_config = ConfigDict(
        extra='forbid',
    )

    hard_skills_text: list[str] = Field(
        default_factory=list,
    )
    soft_skills_text: list[str] = Field(
        default_factory=list,
    )
