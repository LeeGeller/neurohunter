"""Class match mandatory skills vs skills from ResumeFeatures."""

import uuid
from typing import (
    Optional,
)

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.resume import (
    ResumeFeatures,
)
from app.models.vacancy import (
    VacancyRequirements,
)


class MandatorySkillsMatcher:
    """Matcher mandatory skills."""

    def __init__(self, session: AsyncSession):
        """Initialize."""
        self.session = session

    async def get_resume_features(
        self,
        user_id: uuid.UUID,
    ) -> Optional[ResumeFeatures]:
        """Get ResumeFeatures for current user."""

        result = await self.session.execute(
            select(ResumeFeatures).where(
                ResumeFeatures.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()


    async def get_vacancy_requirements(
        self,
        vacancy_id: uuid.UUID,
    ) -> Optional[VacancyRequirements]:
        """Get VacancyRequirements for current user."""

        result = await self.session.execute(
            select(VacancyRequirements).where(
                VacancyRequirements.vacancy_id == vacancy_id,
            )
        )

        return result.scalar_one_or_none()
