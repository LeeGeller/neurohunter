"""Profile routes."""
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import (
    delete,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.models.resume import (
    ResumeDocument,
)
from app.models.user import (
    User,
    UserProfile,
)
from app.schemas.user import (
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
)
from app.services.fastapi_users import (
    current_user,
)
from app.services.resume_parser import (
    ResumeTextExtractor,
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


@router.get(
    '/',
    response_model=UserProfileRead,
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
) -> UserProfileRead:
    """Get user profile."""

    profile = await session.get(UserProfile, user.id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Профиль не найден.',
        )

    return profile


@router.patch(
    '/',
    response_model=UserProfileRead,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    profile_data: UserProfileUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
) -> UserProfileRead:
    """Update user profile."""

    profile = await session.get(UserProfile, user.id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Профиль не найден.',
        )

    for key, value in profile_data.model_dump(
        exclude_unset=True,
    ).items():
        setattr(profile, key, value)

    await session.commit()
    await session.refresh(profile)

    return profile


@router.post(
    '/resume',
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
):
    """Upload and save user resume file."""

    if not file.filename.endswith('.pdf') and not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неподдерживаемый формат файла.',
        )

    extractor = ResumeTextExtractor()
    extraxtored_resume = await extractor.extract(file)

    await session.execute(
        delete(ResumeDocument).where(
            ResumeDocument.user_id == user.id
        ),
    )

    resume = ResumeDocument(
        user_id=user.id,
        text=extraxtored_resume,
    )

    session.add(resume)

    await session.commit()

    return {
        'resume': extraxtored_resume,
    }
