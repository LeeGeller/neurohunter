import uuid

from fastapi_users import (
    schemas,
)
from pydantic import (
    BaseModel,
)


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User read schema."""


class UserCreate(schemas.BaseUserCreate):
    """User create schema."""


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
