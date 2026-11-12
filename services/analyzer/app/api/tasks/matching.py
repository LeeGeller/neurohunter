import asyncio
import uuid
from typing import (
    TYPE_CHECKING,
)

from celery import (
    shared_task,
)

from app.database.mongo_client import (
    MongoDBClient,
)
from app.database.postgres import (
    get_session,
)
from app.matching_service.mandatory_skills_matcher import (
    MandatorySkillsMatcher,
)
from app.models.vacancy_users import (
    VacancyUsers,
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
        # Initialize MandatorySkillsMatcher
        mandatory_skills_matcher = MandatorySkillsMatcher(session=session)

        for vacancy_user in vacancy_users:

            resume_features = await mandatory_skills_matcher.get_resume_features(
                user_id=uuid.UUID(vacancy_user.user_id),
            )
            vacancy_requirements = await mandatory_skills_matcher.get_vacancy_requirements(
                vacancy_id=uuid.UUID(vacancy_user.vacancy_id)
            )

            print(resume_features)
            print(vacancy_requirements)


