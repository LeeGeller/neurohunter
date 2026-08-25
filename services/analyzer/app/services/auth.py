import secrets
from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.user import (
    User,
    UserToken,
)
from services.email import (
    send_verification_email,
)
from utils.security import (
    hash_password,
)


def generate_verification_token() -> str:
    """Generate a verification token."""
    return secrets.token_urlsafe(32)


async def register_user(
    session: AsyncSession,
    email: str,
    password: str
) -> User:
    """Register a new user."""

    result = await session.execute(
        select(User).where(
            User.user_email == email,
        ),
    )

    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует.",
        )

    hashed_password = hash_password(password)

    user = User(
        user_email=email,
        password_hash=hashed_password,
    )

    session.add(user)

    await session.flush()

    token = generate_verification_token()

    users_token = UserToken(
        user_id=user.user_id,
        user_token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    session.add(users_token)

    await session.commit()
    await session.refresh(user)

    await send_verification_email(
        email=user.user_email,
        token=token,
    )

    return user

async def verify_user_by_token(
    session: AsyncSession,
    token: str,
) -> None:
    """Verify user by token."""

    token_result = await session.execute(
        select(UserToken).where(
            UserToken.user_token == token,
        ),
    )

    user_token = token_result.scalar_one_or_none()

    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Токен не найден.",
        )

    if user_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Токен истек.",
        )

    user_result = await session.execute(
        select(User).where(
            User.user_id == user_token.user_id,
        ),
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден.",
        )

    user.is_verified = True

    await session.delete(user_token)
    await session.commit()
