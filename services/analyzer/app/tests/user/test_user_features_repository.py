"""Tests for UserFeatureRepository."""

from uuid import (
    UUID,
)

import pytest

from app.database.postgres import (
    async_session,
)
from app.repositories.user_features_repository import (
    UserFeatureRepository,
)


@pytest.mark.asyncio
async def test_get_user_features_for_search() -> None:
    """Check data returned by the repository."""

    async with async_session() as session:
        repository = UserFeatureRepository(session)
        users = await repository.get_user_features_for_search()

    assert isinstance(users, list)

    for user in users[:10]:
        assert isinstance(user["user_id"], UUID)
        assert isinstance(user["job_titles"], list)
        assert set(user) == {
            "user_id",
            "job_titles",
            "hard_constraints",
        }
