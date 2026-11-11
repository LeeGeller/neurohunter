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
    VacancyRequirementsExtractor,
)
from app.models.vacancy import (
    VacancyFeatures,
    VacancyIdentity,
    VacancyRequirements,
)
from app.repositories.repository_manager import (
    RepositoryManager,
)
from app.schemas.vacancy.vacancy_features import (
    VacancyFeaturesSchema,
)
from app.schemas.vacancy.vacancy_requirements import (
    VacancyRequirementsSchema,
)
from app.services.vacancy_context_service import (
    VacancyContextService,
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

        vacancies_to_analyze = await context_service.get_vacancies_to_analyze()

    finally:
        await mongo_client.disconnect()

    if not vacancies_to_analyze:
        return

    # Initialize extractor
    llm_model = OllamaClient(
        base_url=settings.ollama_host,
        model=settings.ollama_model,
    )

    extractor_vacancy_feature = VacancyFeaturesExtractor(
        llm_client=llm_model,
        response_schema=VacancyFeaturesSchema.model_json_schema(),
    )

    extractor_vacancy_requirements = VacancyRequirementsExtractor(
        llm_client=llm_model,
        response_schema=VacancyRequirementsSchema.model_json_schema(),
    )

    # Initialize PostgreSQL session
    async for session in get_session():

        for vacancy in vacancies_to_analyze:

            try:
                identity = await get_or_create_vacancy_identity(
                    session,
                    external_id=vacancy.id,
                    source=vacancy.url,
                )
                vacancy_uuid = identity.vacancy_uuid

                await process_vacancy_features(
                    session,
                    vacancy,
                    vacancy_uuid,
                    extractor_vacancy_feature,
                )
                await process_vacancy_requirements(
                    session,
                    vacancy,
                    vacancy_uuid,
                    extractor_vacancy_requirements,
                )

                await session.commit()

            except Exception:
                await session.rollback()
                raise


async def process_vacancy_features(
    session,
    vacancy,
    vacancy_uuid,
    extractor: VacancyFeaturesExtractor,
) -> None:
    """Process vacancy features and save them in PostgreSQL."""

    result = await session.execute(
        select(VacancyFeatures).where(
            VacancyFeatures.vacancy_id == vacancy_uuid,
        )
    )

    existing_vacancy_features = result.scalar_one_or_none()

    if existing_vacancy_features:
        return

    features_schema = await extractor.extract_features(
        vacancy,
    )
    vacancy_features = VacancyFeatures(
        vacancy_id=vacancy_uuid,
        **features_schema.model_dump(),
    )

    session.add(vacancy_features)


async def process_vacancy_requirements(
    session,
    vacancy,
    vacancy_uuid,
    extractor: VacancyRequirementsExtractor,
) -> None:
    """Process vacancy requirements and save them in PostgreSQL."""

    result = await session.execute(
        select(VacancyRequirements).where(
            VacancyRequirements.vacancy_id == vacancy_uuid,
        )
    )

    existing_vacancy_requirements = result.scalar_one_or_none()

    if existing_vacancy_requirements:
        return

    requirements_schema = await extractor.extract_requirements(
        vacancy,
    )
    vacancy_requirements = VacancyRequirements(
        vacancy_id=vacancy_uuid,
        **requirements_schema.model_dump(),
    )

    session.add(vacancy_requirements)


async def get_or_create_vacancy_identity(
    session,
    external_id: str,
    source: str,
) -> VacancyIdentity:
    """Get or create a VacancyIdentity in PostgreSQL."""

    result = await session.execute(
        select(VacancyIdentity).where(
            VacancyIdentity.external_id == external_id,
            VacancyIdentity.source == source,
        )
    )

    vacancy_identity = result.scalar_one_or_none()

    if vacancy_identity:
        return vacancy_identity

    vacancy_identity = VacancyIdentity(
        external_id=external_id,
        source=source,
    )

    session.add(vacancy_identity)
    await session.flush()

    return vacancy_identity
