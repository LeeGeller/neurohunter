"""User manager services."""

import uuid
from collections.abc import (
    AsyncGenerator,
)

from fastapi import (
    Depends,
)
from fastapi_users import (
    BaseUserManager,
)

from app.config.settings import (
    settings,
)
from app.models.user import (
    User,
)
from app.services.user_db import (
    get_user_db,
)
from app.services.email import (
    send_verification_email,
)


class UserManager(BaseUserManager[User, uuid.UUID]):
    """User manager."""

    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    def parse_id(self, value: str) -> uuid.UUID:
        return uuid.UUID(value)

    async def on_after_register(
        self,
        user: User,
        request=None,
    ) -> None:
        """Handle actions after registration."""

        await self.request_verify(user, request)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request=None,
    ) -> None:
        """Send verification email."""
        print(f'ON_AFTER_REGISTER: {user.email}')

        await send_verification_email(user.email, token)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """Get user manager."""

    yield UserManager(user_db)
