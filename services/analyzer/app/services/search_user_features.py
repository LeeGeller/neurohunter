"""User features search service."""
import uuid
from collections import (
    defaultdict,
)

from app.repositories.user_features_repository import (
    UserFeatureRepository,
    UserFeatureSearchResult,
)


class SearchUserFeaturesService:
    """Service for searching and grouping user features."""

    def __init__(self, repository: UserFeatureRepository) -> None:
        self.repository = repository

    async def get_user_features(self) -> list[UserFeatureSearchResult]:
        """Retrieve user features for search."""

        return await self.repository.get_user_features_for_search()

    @staticmethod
    def normalized_job_titles(job_titles: list[str]) -> list[str]:
        """Normalize job titles and remove duplicates."""

        return list(
            dict.fromkeys(
                title.strip().casefold()
                for title in job_titles
                if title.strip()
            )
        )

    def group_user_features_by_job_titles(
        self,
        user_features: list[UserFeatureSearchResult],
    ) -> dict[str, list[uuid.UUID]]:
        """Group user IDs by normalized job titles."""

        grouped_users: dict[str, list[uuid.UUID]] = defaultdict(list)

        for user_feature in user_features:
            titles = self.normalized_job_titles(user_feature["job_titles"])

            for title in titles:
                grouped_users[title].append(user_feature["user_id"])

        return dict(grouped_users)

    async def get_group_user_features_by_job_titles(
        self,
    ) -> dict[str, list[uuid.UUID]]:
        """Retrieve user features and group users by job titles."""

        user_features = await self.get_user_features()

        return self.group_user_features_by_job_titles(user_features)
