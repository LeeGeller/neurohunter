from app.llm.client import (
    OllamaClient,
)
from app.llm.service import (
    VacancyFeaturesService,
)
from services.analyzer.app.llm.prompts import (
    VACANCY_FEATURES_PROMPT,
)
from services.analyzer.app.models.vacancy import (
    Vacancy,
)


class VacancyAnalayzer:
    """Analyze vacancies using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_fetures(self, vacancy: Vacancy) -> str:
        """Extract structured features from a vacancy using LLM."""

        promt = VACANCY_FEATURES_PROMPT.format(
            vacancy_id=vacancy.id,
            title=vacancy.title,
            company=vacancy.company,
            work_location=vacancy.work_location or "",
            work_format=vacancy.work_format or "",
            salary_from=vacancy.salary_from or "",
            salary_to=vacancy.salary_to or "",
            description=vacancy.description,
        )

        return await self.llm_client.generate(promt)
