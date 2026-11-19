import asyncio
import uuid

from celery import (
    shared_task,
)
from sqlalchemy import (
    select,
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
    SkillsMatcher,
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


async def _match():
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

            resume_features = await skills_matcher.get_resume_features(
                user_id=uuid.UUID(vacancy_user.user_id),
            )

            vacancy_identity = await session.execute(
                select(
                    VacancyIdentity.vacancy_uuid
                ).where(
                    VacancyIdentity.external_id == vacancy_user.vacancy_id,
                )
            )
            vacancy_id = vacancy_identity.scalar_one_or_none()

            vacancy_requirements = await skills_matcher.get_vacancy_requirements(
                vacancy_id=vacancy_id,
            )

            if resume_features and vacancy_requirements:

                skills_matcher.build_skills_matrix(
                    vacancy_skills=vacancy_requirements.mandatory_skills,
                    resume_skills=resume_features.hard_skills,
                    vacancy_skill_groups=vacancy_requirements.mandatory_skill_groups,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                skills_matcher.calculate_skill_matches()

                skills_matcher.calculate_group_matches(
                    mandatory_skill_groups=vacancy_requirements.mandatory_skill_groups,
                    resume_skills=resume_features.hard_skills,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                mandatory_skill_coverage = skills_matcher.calculate_coverage()
                mandatory_group_coverage = skills_matcher.calculate_group_coverage()

                skills_matcher.build_skills_matrix(
                    vacancy_skills=vacancy_requirements.preferred_skills,
                    resume_skills=resume_features.hard_skills,
                    vacancy_skill_groups=vacancy_requirements.preferred_skill_groups,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                skills_matcher.calculate_skill_matches()
                skills_matcher.calculate_group_matches(
                    mandatory_skill_groups=vacancy_requirements.preferred_skill_groups,
                    resume_skills=resume_features.hard_skills,
                    resume_skill_groups=resume_features.hard_skill_groups,
                )

                prefered_skill_coverage = skills_matcher.calculate_coverage()
                prefered_group_coverage = skills_matcher.calculate_group_coverage()

                experience_matcher = ExperienceMatcher()

                experience_matcher.calculate_experience(
                    vacancy_requirements.experience_min,
                    vacancy_requirements.experience_max,
                    resume_features.experience,
                )

                print('LOW', experience_matcher.low_experience)
                print('HIGH', experience_matcher.high_experience)




