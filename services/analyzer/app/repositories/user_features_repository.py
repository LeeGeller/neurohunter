"""User features repository."""

import uuid
from typing import (
    Optional,
    TypedDict,
    cast,
)

from sqlalchemy import (
    select,
)
from sqlalchemy.engine import (
    RowMapping,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.user import (
    UserFeatures,
    UserProfile,
)


class WorkFormatConstraints(TypedDict):
    """Hard constraints for work formats."""

    remote: Optional[bool]
    office: Optional[bool]
    hybrid: Optional[bool]


class HardConstraints(TypedDict):
    """Structured criteria for primary vacancy filtering."""

    salary: Optional[int]
    experience_years: Optional[float]
    education: Optional[str]
    night_work_tolerance: Optional[str]
    business_trip_tolerance: Optional[str]
    work_format_constraints: WorkFormatConstraints
    physical_activity_tolerance: Optional[str]


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
        """Get user features."""

        statement = (
            select(
                UserFeatures.user_id,
                UserFeatures.job_titles,
                UserFeatures.experience_years,
                UserProfile.salary,
                UserProfile.education,
                UserProfile.experience_years,
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
        rows = cast(list[RowMapping], result.mappings().all())

        return [
            UserFeatureSearchResult(
                user_id=row['user_id'],
                job_titles=row['job_titles'] or [],
                hard_constraints=HardConstraints(
                    salary=row['salary'],
                    experience_years=row['experience_years'],
                    education=row['education'],
                    night_work_tolerance=row['night_work_tolerance'],
                    business_trip_tolerance=row['business_trip_tolerance'],
                    work_format_constraints=row['work_format_constraints'],
                    physical_activity_tolerance=row['physical_activity_tolerance'],
                ),
            )
            for row in rows
        ]
