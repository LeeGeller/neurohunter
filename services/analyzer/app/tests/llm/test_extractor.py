import pytest

from app.config.settings import (
    settings,
)
from app.llm.client import (
    OllamaClient,
)
from app.llm.extractor import (
    VacancyFeaturesExtractor,
)
from app.models.vacancy import (
    Vacancy,
)
from app.models.vacancy_features import (
    VacancyFeatures,
)


@pytest.mark.asyncio
async def test_extract_features():
    print(Vacancy.model_config)
    print(Vacancy.model_fields["vacancy_date"].alias)
    vacancy = Vacancy(
        id="12345",
        title="Python Developer",
        vacancy_date="2026-08-04T10:00:00",
        description="""
        Ищем Python-разработчика.

        Работа 5/2 с 9:00 до 18:00.
        Формат работы гибридный.
        Необходимо взаимодействовать с командой и заказчиками.
        Возможна работа над несколькими задачами одновременно.
        """,
        company="Test Company",
        work_location="Москва",
        work_format="hybrid",
        salary_from=150000,
        salary_to=200000,
        currency="RUB",
        url="https://example.com/vacancy/123",
    )

    llm_client = OllamaClient(
        base_url="http://localhost:11434",
        model=settings.ollama_model,
    )

    extractor = VacancyFeaturesExtractor(llm_client)

    try:
        features = await extractor.extract_features(vacancy)

        assert isinstance(features, VacancyFeatures)
        assert features.vacancy_id == vacancy.id
        assert features.work_days_per_week == 5
        assert features.work_hours_per_day == 8
        assert features.work_format == "hybrid"
        assert features.team_communication is True
        assert features.client_communication is True
        assert features.multitasking_required is True
        print("Extracted features:", features.dict())

    finally:
        await llm_client.close()
