from typing import (
    Optional,
)

from app.llm.client import (
    OllamaClient,
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


class VacancyRequirementsExtractor:
    """Analyze vacancy requirements using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_schema: Optional[dict],
    ) -> None:
        """Initialize the VacancyRequirementsExtractor."""
        self.llm_client = llm_client
        self.response_schema = response_schema

    async def extract_requirements(self, vacancy: Vacancy) -> VacancyRequirementsSchema:
        """Extract structured requirements from a vacancy using LLM."""

        prompt = VACANCY_REQUIREMENTS_PROMPT.format(
            title=vacancy.title,
            description=vacancy.description,
        )

        response = await self.llm_client.generate(
            prompt,
            self.response_schema,
        )

        requirement = VacancyRequirementsSchema.model_validate_json(response)

        return requirement
