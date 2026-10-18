"""Test SearchUserFeaturesService."""

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
from app.services.search_user_features import (
    SearchUserFeaturesService,
)


@pytest.mark.asyncio
async def test_get_grouped_user_features() -> None:
    """Check data returned by the service."""

    async with async_session() as session:
        repository = UserFeatureRepository(session)
        service = SearchUserFeaturesService(repository)
        user_features = await service.get_user_features()

        grouped_user_features_by_job_titles = service.group_user_features_by_job_titles(user_features)

    assert isinstance(grouped_user_features_by_job_titles, dict)

    for job_title, user_ids in grouped_user_features_by_job_titles.items():
        assert isinstance(job_title, str)
        assert isinstance(user_ids, list)
        assert all(isinstance(user_id, UUID) for user_id in user_ids)
