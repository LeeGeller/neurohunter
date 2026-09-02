"""Portfolio features schemas."""
import uuid

from pydantic import (
    BaseModel,
)


class PortfolioFeatures(BaseModel):
    """Portfolio features model for LLM."""

    user_id: uuid.UUID

    # Parameters used for vacancy matching
    job_titles: list[str] = []
    hard_skills: list[str] = []
    soft_skills: list[str] = []
    experience: int | None = None
    projects: list[str] = []
