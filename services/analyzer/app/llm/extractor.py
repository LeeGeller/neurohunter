import json

from app.llm.client import OllamaClient
from app.llm.prompts import VACANCY_FEATURES_PROMPT
from app.models.vacancy import Vacancy
from app.models.vacancy_features import VacancyFeatures

class VacancyFeaturesExtractor:
    """Analyze vacancies using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_features(self, vacancy: Vacancy) -> VacancyFeatures:
        """Extract structured features from a vacancy using LLM."""

        prompt = VACANCY_FEATURES_PROMPT.format(
            vacancy_id=vacancy.id,
            title=vacancy.title,
            company=vacancy.company,
            work_location=vacancy.work_location or "",
            work_format=vacancy.work_format or "",
            salary_from=vacancy.salary_from or "",
            salary_to=vacancy.salary_to or "",
            description=vacancy.description,
        )

        response = await self.llm_client.generate(prompt)

        return VacancyFeatures(**json.loads(response))
