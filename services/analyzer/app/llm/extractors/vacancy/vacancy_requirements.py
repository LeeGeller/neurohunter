"""VacancyRequirements extractor using LLM."""

import asyncio

from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.extractors.knowledge.concept_extraction import (
    ConceptExtractor,
)
from app.llm.prompts import (
    VACANCY_REQUIREMENTS_PROMPT,
)
from app.models.vacancy import (
    Vacancy,
)
from app.schemas.knowledge.concept_extraction import (
    ConceptExtractionSchema,
)
from app.schemas.knowledge.vacancy_requirements_classification import (
    VacancyRequirementsClassificationSchema,
)
from app.schemas.vacancy.vacancy_requirements import (
    VacancyRequirementsSchema,
)


class VacancyRequirementsExtractor(
    BaseExtractor[VacancyRequirementsClassificationSchema]
):
    """Analyze vacancy requirements using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        concept_extractor: ConceptExtractor,
    ) -> None:
        """Initialize the VacancyRequirementsExtractor."""

        super().__init__(
            llm_client=llm_client,
            response_model=VacancyRequirementsClassificationSchema,
        )

        self.concept_extractor = concept_extractor

    async def _extract_concepts(
        self,
        source_text: list[str],
    ) -> ConceptExtractionSchema:
        """Extract professional concepts from classified text fragments."""

        if not source_text:
            return ConceptExtractionSchema()

        return await self.concept_extractor.extract(
            source_text='\n'.join(source_text),
        )


    async def extract_requirements(
        self,
        vacancy: Vacancy,
    ) -> VacancyRequirementsSchema:
        """Extract structured requirements from a vacancy."""

        prompt = VACANCY_REQUIREMENTS_PROMPT.format(
            title=vacancy.title,
            description=vacancy.description,
        )

        classification = await self.generate(prompt=prompt)

        mandatory, preferred = await asyncio.gather(
            self._extract_concepts(classification.mandatory_text),
            self._extract_concepts(classification.preferred_text),
        )

        data = classification.model_dump(
            exclude={
                'mandatory_text',
                'preferred_text',
            },
        )

        data.update(
            {
                'mandatory_skills': mandatory.concepts,
                'mandatory_skill_groups': mandatory.concept_groups,
                'preferred_skills': preferred.concepts,
                'preferred_skill_groups': preferred.concept_groups,
            },
        )

        return VacancyRequirementsSchema.model_validate(data)
