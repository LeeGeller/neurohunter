"""ResumeFeatures extractor using LLM."""

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
    CONCEPT_EXTRACTION_PROMPT,
    RESUME_FEATURES_PROMPT,
)
from app.schemas.knowledge.concept_extraction import (
    ConceptExtractionSchema,
)
from app.schemas.knowledge.resume_skill_classification import (
    ResumeSkillClassificationSchema,
)
from app.schemas.user.resume_data import (
    ResumeDataSchema,
)
from app.schemas.user.resume_features import (
    ResumeFeaturesSchema,
)


class ResumeFeaturesExtractor(BaseExtractor[ResumeDataSchema]):
    """Analyze resumes using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        concept_extractor: ConceptExtractor,
    ) -> None:
        """Initialize the ResumeFeaturesExtractor."""

        super().__init__(
            llm_client=llm_client,
            response_model=ResumeDataSchema,
        )

        self.concept_extractor = concept_extractor

        self.skill_classifier = BaseExtractor(
            llm_client=llm_client,
            response_model=ResumeSkillClassificationSchema,
        )

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

    async def extract_features(self, resume: str) -> ResumeFeaturesSchema:
        """Extract structured features from a resume."""

        data_prompt = RESUME_FEATURES_PROMPT.replace(
            '{resume_text}',
            resume,
        )

        resume_data = await self.generate(prompt=data_prompt)

        hard_skills_prompt = CONCEPT_EXTRACTION_PROMPT.replace(
            '{source_text}',
            '\n'.join(resume_data.hard_skills),
        )

        soft_skills_prompt = CONCEPT_EXTRACTION_PROMPT.replace(
            '{source_text}',
            '\n'.join(resume_data.soft_skills),
        )

        hard_skills, soft_skills = await asyncio.gather(
            self.concept_extractor.generate(prompt=hard_skills_prompt),
            self.concept_extractor.generate(prompt=soft_skills_prompt),
        )

        resume_data.hard_skills = hard_skills.concepts

        resume_data.soft_skills = soft_skills.concepts

        return ResumeFeaturesSchema.model_validate(resume_data.model_dump())
