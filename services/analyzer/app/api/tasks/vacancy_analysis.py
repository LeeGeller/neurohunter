import asyncio

from celery import (
    shared_task,
)
from sqlalchemy import (
    select,
)

from app.config.settings import (
    settings,
)
from app.database.mongo_client import (
    MongoDBClient,
)
from app.database.postgres import (
    get_session,
)
from app.llm.client import (
    OllamaClient,
)
from app.llm.extractor import (
    VacancyFeaturesExtractor,
)
from app.models.vacancy import (
    VacancyFeatures,
)
from app.repositories.repository_manager import (
    RepositoryManager,
)
from app.services.vacancy_context_service import (
    VacancyContextService,
)
from app.utils.json_schema import (
    build_json_schema,
)


@shared_task
def analyze_vacancies_task() -> None:
    """Celery task to analyze vacancies."""
    asyncio.run(_analyze_vacancies())


async def _analyze_vacancies() -> None:
    """Analyze vacancies and save their features in PostgreSQL."""

    # Initialize MongoDB client
    mongo_client = MongoDBClient()
    await mongo_client.connect()

    try:
        repositories = RepositoryManager(mongo_client)
        context_service = VacancyContextService(repositories)

        vacancies = await context_service.get_all_vacancy_users()

        all_vacancies = await context_service.get_all_vacancies()

    finally:
        await mongo_client.disconnect()

    if not vacancies:
        return

    # Initialize extractor
    llm_model = OllamaClient(
        base_url=settings.ollama_host,
        model=settings.ollama_model,
        response_schema=build_json_schema(VacancyFeatures),
    )

    extractor = VacancyFeaturesExtractor(
        llm_client=llm_model,
    )

    # Initialize PostgreSQL session
    async for session in get_session():

        for vacancy in all_vacancies:
            # Extract vacancy features using LLM
            vacancy_feature = await extractor.extract_features(vacancy)

            # Check whether features already exist
            result = await session.execute(
                select(VacancyFeatures).where(
                    VacancyFeatures.vacancy_id == vacancy_feature.vacancy_id,
                ),
            )

            old_vacancy_feature = result.scalar_one_or_none()

            if old_vacancy_feature:
                # Update existing ORM object
                for field, value in vacancy_feature.items():
                    setattr(old_vacancy_feature, field, value)

            else:
                # Create new ORM object
                session.add(vacancy_feature)

            await session.commit()
