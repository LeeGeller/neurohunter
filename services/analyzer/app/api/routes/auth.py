from fastapi import (
    APIRouter,
    Depends,
)

from app.schemas.auth import (
    UserResponse,
)
from app.services.auth_backend import (
    auth_backend,
)
from app.services.fastapi_users import (
    current_user,
    fastapi_users,
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)


@router.get('/current-user')
async def get_current_user(
    user: UserResponse = Depends(current_user)
) -> UserResponse:
    return user
