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
    UserManager,
    get_user_manager,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
