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
    """Service for searching user features.

    Group user features by user_id and job_titles. Return a dict with job_titles as keys
    and a list of user_ids as values.

    Attributes:
        repository: Repository for retrieving user features.
    """

    def __init__(self, repository: UserFeatureRepository) -> None:
        self.repository = repository


    async def get_user_features(self) -> list[UserFeatureSearchResult]:
        """Get user features for search."""

        user_features = await self.repository.get_user_features_for_search()

        return user_features

    @staticmethod
    def normalized_job_titles(job_titles: list[str]) -> list[str]:
        """Normalize job titles and remove duplicates."""

        return list(
            dict.fromkeys(
                job_title.strip().casefold()
                for job_title in job_titles
                if job_title.strip()
            )
        )

    @staticmethod
    def group_user_features_by_job_titles(
        user_features: list[UserFeatureSearchResult],
    ) -> dict[str, list[uuid.UUID]]:
        """Group user features by job_titles.

        Returns:
            Dict with job_titles as keys and a list of user_ids as values.
        """

        grouped_users_by_job_titles: dict[str, list[uuid.UUID]] = defaultdict(list)

        for user_feature in user_features:
            normalized_job_titles = SearchUserFeaturesService.normalized_job_titles(user_feature["job_titles"])
            for job_title in normalized_job_titles:
                grouped_users_by_job_titles[job_title].append(user_feature["user_id"])

        return grouped_users_by_job_titles
