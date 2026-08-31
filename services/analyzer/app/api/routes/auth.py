from fastapi import (
    APIRouter,
)

from app.schemas.auth import (
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

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
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
