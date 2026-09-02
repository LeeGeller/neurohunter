"""User features schemas."""

import uuid

from pydantic import (
    BaseModel,
)


class UserFeatures(BaseModel):
    """User features model for LLM."""

    user_id: uuid.UUID

    # Parameters used for vacancy matching
    hard_constraints: list[str] = []
    preferences: list[str] = []
    tolerances: list[str] = []

    # Additional context for LLM to better understand the user
    context: list[str] = []
