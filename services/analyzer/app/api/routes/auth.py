from collections.abc import (
    AsyncGenerator,
)

from fastapi import (
    APIRouter,

)

from app.database.postgres import (
    get_session,
)
from app.schemas.auth import (
    UserRegister,
)


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


