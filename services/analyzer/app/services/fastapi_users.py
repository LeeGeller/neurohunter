"""Users services."""
import uuid

from fastapi_users import (
    FastAPIUsers,
)

from app.models.user import (
    User,
)
from app.services.auth_backend import (
    auth_backend,
)
from app.services.user_manager import (
    get_user_manager,
)
from app.schemas.auth import (
    UserRead,
)



fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
verification_router = fastapi_users.get_verify_router(UserRead)
