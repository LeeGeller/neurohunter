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
        self.matrix: list[list[int]] = []
        self.skill_matches: list[int] = []
        self.coverage: float = 0.0

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

    def build_skills_matrix(
        self,
        mandatory_skills: list[str],
        resume_skills: list[str],
        ):
        """Build a binary matrix of mandatory skills and resume skills.

        Each row represents a mandatory skill required by the vacancy.
        Each column represents a skill extracted from the candidate's resume.

        A matrix cell contains:
            1 - if the mandatory skill matches the resume skill;
            0 - otherwise.

        The resulting matrix has N × M dimensions, where:
            N - number of mandatory skills;
            M - number of resume skills.

        Example:
            mandatory_skills = ['Python', 'Django']
            resume_skills = ['Python', 'Django', 'PostgreSQL', 'Redis']

            Result:
            [
                [1, 0, 0, 0],  # Python
                [0, 1, 0, 0],  # Django
            ]

        Additional skills in the resume do not increase mandatory skills
        coverage. They are represented by columns but do not correspond
        to any additional vacancy requirements.
        """

        self.matrix = [
            [
                int(mandatory == resume)
                for resume in resume_skills
            ]
            for mandatory in mandatory_skills
        ]

    def calculate_skill_matches(self) -> None:
        """Calculate binary coverage indicators for mandatory skills.

        Each element represents one mandatory skill:
            1 - the skill is present in the resume;
            0 - the skill is missing from the resume.

        The result contains one indicator per mandatory skill.
        """
        self.skill_matches = [
            max(row, default=0)
            for row in self.matrix
        ]

    def calculate_coverage(self) -> float:
        """Calculate the proportion of mandatory skills covered by the resume.

        Coverage is calculated as the ratio of matched mandatory skills
        to the total number of mandatory skills.

        Returns:
            float: Coverage ratio between 0.0 and 1.0.
            Returns 0.0 if there are no mandatory skills.
        """
        if not self.skill_matches:
            self.coverage = 0.0
        else:
            self.coverage = (
                sum(self.skill_matches) / len(self.skill_matches)
            )

        return self.coverage
