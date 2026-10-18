"""User features repository."""

import uuid
from typing import (
    TypedDict,
)


from pydantic import (
    JsonValue,
)
from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.user import (
    UserFeatures,
)


class UserFeatureSearchResult(TypedDict):
    """User feature search result."""

    user_id: uuid.UUID
    job_titles: list[str]
    hard_constraints: list[dict[str, JsonValue]]


class UserFeatureRepository:
    """Repository for retrieving user features."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_features_for_search(self) -> list[UserFeatureSearchResult]:
        """Get user features for search."""

        statement = select(
            UserFeatures.user_id,
            UserFeatures.job_titles,
            UserFeatures.hard_constraints,
        )

        result = await self.session.execute(statement)
        rows = result.mappings().all()
        print(rows)

        return rows
