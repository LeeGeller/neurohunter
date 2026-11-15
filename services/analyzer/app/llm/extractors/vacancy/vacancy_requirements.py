"""VacancyRequirements extractor using LLM."""

from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.prompts import (
    VACANCY_REQUIREMENTS_PROMPT,
)
from app.models.vacancy import (
    Vacancy,
)
from app.schemas.vacancy.vacancy_requirements import (
    VacancyRequirementsSchema,
)


class VacancyRequirementsExtractor(
    BaseExtractor[VacancyRequirementsSchema]
):
    """Analyze vacancy requirements using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
    ) -> None:
        """Initialize the VacancyRequirementsExtractor."""

        super().__init__(
            llm_client=llm_client,
            response_model=VacancyRequirementsSchema,
        )

    async def extract_requirements(self, vacancy: Vacancy) -> VacancyRequirementsSchema:
        """Extract structured requirements from a vacancy using LLM."""

        prompt = VACANCY_REQUIREMENTS_PROMPT.format(
            title=vacancy.title,
            description=vacancy.description,
        )

        return await self.generate(prompt)
