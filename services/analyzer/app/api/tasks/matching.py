import asyncio
import uuid

from celery import (
    shared_task,
)
from sqlalchemy import (
    select,
)
from sqlalchemy.dialects.postgresql import (
    insert,
)

from app.database.mongo_client import (
    MongoDBClient,
)
from app.database.postgres import (
    get_session,
)
from app.matching_service.experience_matcher import (
    ExperienceMatcher,
)
from app.matching_service.skills_matcher import (
    Skill,
    SkillGroup,
    SkillsMatcher,
)
from app.models.professional_fit import (
    ProfessionalFit,
)
from app.models.vacancy import (
    VacancyIdentity,
)
from app.repositories.repository_manager import (
    RepositoryManager,
)
from app.services.vacancy_context_service import (
    VacancyContextService,
)


@shared_task
def run_match() -> None:
    """Celery task to match vacancies vs users."""

    asyncio.run(
        _match(),
    )


async def _match() -> None:
    """Match vacancies vs users."""

    # Initialize MongoDBClient
    mongo_client = MongoDBClient()
    await mongo_client.connect()

    # Get VacancyUsers from MongoDB with VacancyContextService
    try:
        repositories = RepositoryManager(mongo_client)
        context_service = VacancyContextService(
            repositories.vacancy,
            repositories.vacancy_users,
        )

        vacancy_users = await context_service.get_all_vacancy_users()

    finally:
        await mongo_client.disconnect()

    async for session in get_session():

        # Initialize SkillsMatcher
        skills_matcher = SkillsMatcher(session=session)

        for vacancy_user in vacancy_users:

            async with session.begin():

                resume_features = await skills_matcher.get_resume_features(
                    user_id=uuid.UUID(vacancy_user.user_id),
                )

                if not resume_features:
                    continue

                vacancy_identity = await session.execute(
                    select(
                        VacancyIdentity.vacancy_uuid,
                    ).where(
                        VacancyIdentity.external_id == vacancy_user.vacancy_id,
                    )
                )

                vacancy_id = vacancy_identity.scalar_one_or_none()

                if vacancy_id is None:
                    continue

                vacancy_requirements = await skills_matcher.get_vacancy_requirements(
                    vacancy_id=vacancy_id,
                )

                if not vacancy_requirements:
                    continue

                # Get fields for ProfessionalFit
                mandatory_skill_coverage, mandatory_group_coverage = match_skills(
                    skills_matcher=skills_matcher,
                    vacancy_skills=vacancy_requirements.mandatory_skills,
                    resume_skills=resume_features.hard_skills,
                    vacancy_skill_groups=vacancy_requirements.mandatory_skill_groups,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                preferred_skills_coverage, preferred_skill_groups_coverage = match_skills(
                    skills_matcher=skills_matcher,
                    vacancy_skills=vacancy_requirements.preferred_skills,
                    resume_skills=resume_features.hard_skills,
                    vacancy_skill_groups=vacancy_requirements.preferred_skill_groups,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                if (
                    mandatory_skill_coverage == 0.0
                    and mandatory_group_coverage == 0.0
                ):
                    continue

                experience_matcher = ExperienceMatcher()

                experience_matcher.calculate_experience(
                    vacancy_requirements.experience_min,
                    vacancy_requirements.experience_max,
                    resume_features.experience,
                )

                if experience_matcher.low_experience:
                    continue

                stmt = insert(ProfessionalFit).values(
                    resume_id=resume_features.user_id,
                    vacancy_requirements_id=vacancy_requirements.id,
                    mandatory_skills_coverage=mandatory_skill_coverage,
                    mandatory_skill_groups_coverage=mandatory_group_coverage,
                    preferred_skills_coverage=preferred_skills_coverage,
                    preferred_skill_groups_coverage=preferred_skill_groups_coverage,
                    low_experience=experience_matcher.low_experience,
                    high_experience=experience_matcher.high_experience,
                )

                stmt = stmt.on_conflict_do_update(
                    constraint='uq_professional_fit_resume_id_vacancy_requirements_id',
                    set_={
                        'mandatory_skills_coverage': stmt.excluded.mandatory_skills_coverage,
                        'mandatory_skill_groups_coverage': stmt.excluded.mandatory_skill_groups_coverage,
                        'preferred_skills_coverage': stmt.excluded.preferred_skills_coverage,
                        'preferred_skill_groups_coverage': stmt.excluded.preferred_skill_groups_coverage,
                        'low_experience': stmt.excluded.low_experience,
                        'high_experience': stmt.excluded.high_experience,
                    },
                )

                await session.execute(stmt)


def match_skills(
    skills_matcher: SkillsMatcher,
    vacancy_skills: list[Skill],
    resume_skills: list[Skill],
    vacancy_skill_groups: list[SkillGroup],
    resume_skill_groups: list[SkillGroup],
) -> tuple[float, float]:
    """Return coverage for individual skills and skill groups."""

    skills_matcher.build_skills_matrix(
        vacancy_skills=vacancy_skills,
        resume_skills=resume_skills,
        vacancy_skill_groups=vacancy_skill_groups,
        resume_skill_groups=resume_skill_groups,
    )

    skills_matcher.calculate_skill_matches()
    skills_matcher.calculate_group_matches()

    return (
        skills_matcher.calculate_coverage(),
        skills_matcher.calculate_group_coverage(),
    )
