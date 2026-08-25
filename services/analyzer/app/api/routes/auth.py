from fastapi import (
    APIRouter,
    Depends,
    status,
    Query,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.schemas.auth import (
    UserRegister,
)
from app.services.auth import (
    register_user,
    verify_user_by_token,
)


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_session),
):
    """Register a new user."""

    await register_user(
        session=db,
        email=user_data.email,
        password=user_data.password,
    )

    return {
        'email': user_data.email,
    }

@router.get('/verify')
async def verify_user(
    token: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    """Verify user by token."""

    await verify_user_by_token(
        session=db,
        token=token,
    )

    return {
        'message': 'Email успешно подтверждён.',
    }
