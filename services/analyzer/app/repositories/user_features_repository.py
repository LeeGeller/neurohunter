"""User features repository."""

import uuid
from typing import (
    TypedDict,
)

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.user import (
    UserFeatures,
    UserProfile,
)
from app.schemas.work_format import (
    WorkFormatConstraints,
)


class HardConstraints(TypedDict):
    """Structured criteria for primary vacancy filtering."""

    salary: int | None
    experience_years: float | None
    education: str | None
    night_work_tolerance: str | None
    business_trip_tolerance: str | None
    work_format_constraints: WorkFormatConstraints
    physical_activity_tolerance: str | None


class UserFeatureSearchResult(TypedDict):
    """User feature search result."""

    user_id: uuid.UUID
    job_titles: list[str]
    hard_constraints: HardConstraints


class UserFeatureRepository:
    """Repository for retrieving user features."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_features_for_search(self) -> list[UserFeatureSearchResult]:
        """Get user features for search."""

        statement = (
            select(
                UserFeatures.user_id,
                UserFeatures.job_titles,
                UserProfile.salary,
                UserProfile.experience_years,
                UserProfile.education,
                UserProfile.night_work_tolerance,
                UserProfile.business_trip_tolerance,
                UserProfile.work_format_constraints,
                UserProfile.physical_activity_tolerance,
            )
            .join(
                UserProfile,
                UserProfile.user_id == UserFeatures.user_id,
            )
        )

        result = await self.session.execute(statement)
        rows = result.mappings().all()

        return [
            {
                "user_id": row["user_id"],
                "job_titles": row["job_titles"] or [],
                "hard_constraints": {
                    "salary": row["salary"],
                    "experience_years": row["experience_years"],
                    "education": row["education"],
                    "night_work_tolerance": row["night_work_tolerance"],
                    "business_trip_tolerance": row["business_trip_tolerance"],
                    "work_format_constraints": row["work_format_constraints"] or {
                        "remote": None,
                        "office": None,
                        "hybrid": None,
                    },
                    "physical_activity_tolerance": (
                        row["physical_activity_tolerance"]
                    ),
                },
            }
            for row in rows
        ]
