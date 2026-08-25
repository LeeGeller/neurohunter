from pydantic import (
    BaseModel,
    EmailStr,
)

class UserRegister(BaseModel):
    """User registration schema."""

    email: EmailStr


class UserRegisterToken(BaseModel):
    """User register token model schema."""

    token: str


class UserRespons(BaseModel):
    """User response schema."""

    user_id: str
    email: EmailStr
    is_verified: bool
