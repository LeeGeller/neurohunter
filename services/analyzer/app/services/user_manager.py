"""User manager services."""

import uuid

from fastapi_users import (
    BaseUserManager,
)

from app.models.user import (
    User,
)
from app.services.user_db import (
    get_user_db,
)
from services.analyzer.app.config import (
    settings,
)


class UserManager(BaseUserManager[User, uuid.UUID]):
    """User manager."""

    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request=None,
    ) -> None:
        print(f'Пользователь {user.id} зарегистрирован.')

    async def get_user_manager(
        user_db=Depends(get_user_db),
    ):
        """Get user manager."""

        yield UserManager(user_db)
