"""User services."""

from collections.abc import (
    AsyncGenerator,
)
from uuid import UUID

from fastapi import (
    Depends,
)
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.models.user import (
    User,
)


async def get_user_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, UUID], None]:
    """Get user database."""

    yield SQLAlchemyUserDatabase(session, User)
