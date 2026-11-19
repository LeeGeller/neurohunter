"""Class match mandatory skills vs skills from ResumeFeatures."""

import uuid
from typing import (
    Optional,
    TypedDict,
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


class Skill(TypedDict):
    """Represent an independently extracted skill."""

    source_text: str
    canonical_name: str


class SkillGroupOption(TypedDict):
    """Represent a skill inside a logical group."""

    canonical_name: str


class SkillGroup(TypedDict):
    """Represent a group of skills connected by a logical operator."""

    source_text: str
    operator: str
    options: list[SkillGroupOption]


class SkillsMatcher:
    """Match mandatory vacancy skills against resume skills."""

    def __init__(self, session: AsyncSession):
        """Initialize matcher."""

        self.session = session

        # Individual skills matrix.
        self.matrix: list[list[int]] = []

        # Logical groups matrix.
        self.group_matrix: list[list[int]] = []

        # Individual skill matching results.
        self.skill_matches: list[int] = []

        # Logical group matching results.
        self.group_matches: list[int] = []

        # Coverage metrics.
        self.coverage: float = 0.0
        self.group_coverage: float = 0.0

        # Prepared data for matching.
        self._vacancy_skill_groups: list[SkillGroup] = []
        self._confirmed_resume_skills: set[str] = set()

        # Indices of individual requirements not represented
        # by logical groups.
        self._standalone_skill_indices: list[int] = []

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
        """Get VacancyRequirements for current vacancy."""

        result = await self.session.execute(
            select(VacancyRequirements).where(
                VacancyRequirements.vacancy_id == vacancy_id,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    def normalize_skill_name(value: str) -> str:
        """Normalize skill name for exact string comparison."""

        return ' '.join(value.casefold().split())

    @classmethod
    def _get_skill_names(
        cls,
        skills: list[Skill],
    ) -> set[str]:
        """Extract normalized canonical skill names."""

        return {
            cls.normalize_skill_name(skill['canonical_name'])
            for skill in skills
            if skill.get('canonical_name')
        }

    @classmethod
    def _get_group_options(
        cls,
        group: SkillGroup,
    ) -> set[str]:
        """Extract normalized canonical names from a group."""

        return {
            cls.normalize_skill_name(option['canonical_name'])
            for option in group.get('options', [])
            if option.get('canonical_name')
        }

    @classmethod
    def _get_grouped_skill_names(
        cls,
        groups: list[SkillGroup],
    ) -> set[str]:
        """Get all skill names represented in logical groups."""

        return {
            skill_name
            for group in groups
            for skill_name in cls._get_group_options(group)
        }

    @classmethod
    def _get_confirmed_resume_skills(
        cls,
        resume_skills: list[Skill],
        resume_skill_groups: list[SkillGroup],
    ) -> set[str]:
        """Get skills that can be treated as individually confirmed.

        Skills belonging exclusively to OR groups are not considered
        individually confirmed.

        AND groups confirm all their options.
        """

        resume_names = cls._get_skill_names(resume_skills)

        alternative_names = {
            skill_name
            for group in resume_skill_groups
            if group['operator'] == 'OR'
            for skill_name in cls._get_group_options(group)
        }

        return resume_names - alternative_names

    @classmethod
    def _group_matches_group(
        cls,
        mandatory_group: SkillGroup,
        resume_group: SkillGroup,
    ) -> bool:
        """Check whether a resume group satisfies a vacancy group."""

        mandatory_options = cls._get_group_options(
            mandatory_group,
        )

        resume_options = cls._get_group_options(
            resume_group,
        )

        if not mandatory_options or not resume_options:
            return False

        mandatory_operator = mandatory_group['operator']
        resume_operator = resume_group['operator']

        if mandatory_operator == 'AND':
            # An OR group cannot prove that all required skills
            # are possessed by the candidate.
            if resume_operator == 'OR':
                return False

            return mandatory_options.issubset(resume_options)

        if mandatory_operator == 'OR':
            if resume_operator == 'AND':
                # At least one required alternative is confirmed.
                return bool(
                    mandatory_options & resume_options,
                )

            if resume_operator == 'OR':
                # Every candidate alternative must be acceptable
                # for the vacancy requirement.
                return resume_options.issubset(mandatory_options)

        return False

    @classmethod
    def _group_is_covered(
        cls,
        mandatory_group: SkillGroup,
        confirmed_resume_skills: set[str],
        resume_skill_groups: list[SkillGroup],
    ) -> bool:
        """Check whether a vacancy group is covered by the resume."""

        mandatory_options = cls._get_group_options(
            mandatory_group,
        )

        if not mandatory_options:
            return False

        operator = mandatory_group['operator']

        # First, check independently confirmed resume skills.
        matched_options = mandatory_options & confirmed_resume_skills

        if operator == 'AND':
            if mandatory_options.issubset(confirmed_resume_skills):
                return True

            # An AND requirement can also be satisfied by
            # a resume AND group containing all required skills.
            return any(
                cls._group_matches_group(
                    mandatory_group,
                    resume_group,
                )
                for resume_group in resume_skill_groups
            )

        if operator == 'OR':
            if matched_options:
                return True

            # An OR requirement can be satisfied by a resume OR group
            # only when all its alternatives are accepted by the vacancy.
            return any(
                cls._group_matches_group(
                    mandatory_group,
                    resume_group,
                )
                for resume_group in resume_skill_groups
            )

        return False

    def build_skills_matrix(
        self,
        vacancy_skills: list[Skill],
        resume_skills: list[Skill],
        vacancy_skill_groups: Optional[list[SkillGroup]] = None,
        resume_skill_groups: Optional[list[SkillGroup]] = None,
    ) -> None:
        """Build individual skill and logical group matrices."""

        vacancy_skill_groups = vacancy_skill_groups or []
        resume_skill_groups = resume_skill_groups or []

        # Reset previous matching state.
        self.matrix = []
        self.group_matrix = []
        self.skill_matches = []
        self.group_matches = []
        self.coverage = 0.0
        self.group_coverage = 0.0
        self._standalone_skill_indices = []

        vacancy_names = [
            self.normalize_skill_name(skill['canonical_name'])
            for skill in vacancy_skills
        ]

        self._vacancy_skill_groups = vacancy_skill_groups

        self._confirmed_resume_skills = self._get_confirmed_resume_skills(
            resume_skills,
            resume_skill_groups,
        )

        confirmed_resume_names = sorted(
            self._confirmed_resume_skills,
        )

        vacancy_grouped_names = self._get_grouped_skill_names(
            vacancy_skill_groups,
        )

        # Identify standalone vacancy requirements.
        self._standalone_skill_indices = [
            index
            for index, skill_name in enumerate(vacancy_names)
            if skill_name not in vacancy_grouped_names
        ]

        # Build individual skill matrix.
        self.matrix = [
            [
                int(vacancy == resume)
                for resume in confirmed_resume_names
            ]
            for vacancy in vacancy_names
        ]

        # Build logical group matrix.
        self.group_matrix = [
            [
                int(
                    self._group_matches_group(
                        vacancy_group,
                        resume_group,
                    )
                )
                for resume_group in resume_skill_groups
            ]
            for vacancy_group in vacancy_skill_groups
        ]

    def calculate_skill_matches(self) -> None:
        """Calculate binary matches for individual vacancy skills."""

        self.skill_matches = [
            max(row, default=0)
            for row in self.matrix
        ]

    def calculate_group_matches(self) -> None:
        """Calculate binary matches for logical vacancy groups."""

        self.group_matches = []

        for index, vacancy_group in enumerate(
            self._vacancy_skill_groups,
        ):
            vacancy_options = self._get_group_options(
                vacancy_group,
            )

            if not vacancy_options:
                self.group_matches.append(0)
                continue

            operator = vacancy_group['operator']

            matched_options = (
                vacancy_options & self._confirmed_resume_skills
            )

            group_matrix_matches = any(
                self.group_matrix[index],
            )

            if operator == 'AND':
                is_matched = (
                    vacancy_options.issubset(
                        self._confirmed_resume_skills,
                    )
                    or group_matrix_matches
                )

            elif operator == 'OR':
                is_matched = (
                    bool(matched_options)
                    or group_matrix_matches
                )

            else:
                is_matched = False

            self.group_matches.append(
                int(is_matched),
            )

    def calculate_coverage(self) -> float:
        """Calculate coverage of standalone mandatory skills.

        Skills belonging to logical groups are excluded from this
        metric because they are evaluated separately by group_coverage.

        Returns:
            float: Coverage ratio between 0.0 and 1.0.
        """

        standalone_matches = [
            self.skill_matches[index]
            for index in self._standalone_skill_indices
        ]

        if not standalone_matches:
            self.coverage = 0.0
        else:
            self.coverage = (
                sum(standalone_matches) / len(standalone_matches)
            )

        return self.coverage

    def calculate_group_coverage(self) -> float:
        """Calculate coverage of mandatory logical groups.

        Returns:
            float: Coverage ratio between 0.0 and 1.0.
        """

        if not self.group_matches:
            self.group_coverage = 0.0
        else:
            self.group_coverage = (
                sum(self.group_matches) / len(self.group_matches)
            )

        return self.group_coverage
