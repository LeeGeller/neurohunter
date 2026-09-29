"""User features schemas."""

import uuid
from typing import (
    Union,
)

from pydantic import (
    BaseModel,
    Field,
)


class UserFeatures(BaseModel):
    """User features model for LLM."""

    user_id: uuid.UUID

    job_titles: list[str] = Field(
        default_factory=list,
    )

    # Parameters used for vacancy matching
    hard_constraints: list[dict[str, Union[int, float]]] = Field(
        default_factory=list,
    )
    preferences: list[str] = Field(
        default_factory=list,
    )
    tolerances: list[str] = Field(
        default_factory=list,
    )

    # Additional context for LLM to better understand the user
    context: list[str] = Field(
        default_factory=list,
    )
