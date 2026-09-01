"""Profile routes."""

from typing import (
    TYPE_CHECKING,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.models.user import (
    User,
    UserProfile,
)
from app.schemas.user import (
    UserProfileCreate,
    UserProfileRead,
)
from app.services.fastapi_users import (
    current_user,
)

router = APIRouter(
    prefix='/profile',
    tags=['Profile'],
)


@router.post(
    '/',
    response_model=UserProfileRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile_data: UserProfileCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
) -> UserProfileRead:
    """Create user profile."""

    profile = UserProfile(
        user_id=user.id,
        **profile_data.model_dump(),
    )

    session.add(profile)

    await session.commit()
    await session.refresh(profile)

    return profile
