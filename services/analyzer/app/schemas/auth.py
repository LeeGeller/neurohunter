import uuid

from pydantic import (
    BaseModel,
    EmailStr,
)


class UserResponse(BaseModel):
    """User response schema."""

    user_id: uuid.UUID
    email: EmailStr
    is_verified: bool
