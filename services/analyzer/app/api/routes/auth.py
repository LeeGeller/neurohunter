from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.models.user import (
    RefreshToken,
    User,
)
from app.schemas.auth import (
    TokenResponse,
    UserCreate,
    UserRead,
)
from app.services.auth_backend import (
    auth_backend,
)
from app.services.fastapi_users import (
    fastapi_users,
    verification_router,
)
from app.services.refresh_token import (
    create_refresh_token,
    hash_refresh_token,
)
from app.services.user_manager import (
    get_user_manager,
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    '/login',
    response_model=TokenResponse,
)


async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager=Depends(get_user_manager),
    strategy=Depends(auth_backend.get_strategy),
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Authenticate user and return access and refresh tokens."""

    user = await user_manager.authenticate(credentials)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Login failed.',
        )

    access_token = await strategy.write_token(
        user,
    )

    refresh_token, refresh_token_hash = create_refresh_token()

    db_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=refresh_token_hash,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    session.add(db_refresh_token)

    await session.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    '/refresh',
    response_model=TokenResponse,
)
async def refresh(
    refresh_token: str,
    strategy=Depends(auth_backend.get_strategy),
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Refresh access token."""

    token_hash = hash_refresh_token(refresh_token)

    result = await session.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
        )
    )

    db_refresh_token = result.scalar_one_or_none()

    if not db_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token.',
        )

    now = datetime.now(timezone.utc)

    if db_refresh_token.expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired.',
        )

    result = await session.execute(
        select(User).where(
            User.id == db_refresh_token.user_id,
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found.',
        )

    access_token = await strategy.write_token(
        user,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

router.include_router(
    verification_router,
)
