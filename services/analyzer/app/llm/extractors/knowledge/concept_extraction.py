"""Concept extractor."""


from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.prompts import (
    CONCEPT_EXTRACTION_PROMPT,
)
from app.schemas.knowledge.concept_extraction import (
    ConceptExtractionSchema,
)


class ConceptExtractor(BaseExtractor[ConceptExtractionSchema]):
    """Extract professional concepts from text."""

    def __init__(self, llm_client: OllamaClient):
        """Initialize."""

        super().__init__(
            llm_client=llm_client,
            response_model=ConceptExtractionSchema,
        )

    async def extract(
        self,
        source_text: str,
    ) -> ConceptExtractionSchema:
        """Extract concepts from source text."""

        prompt = CONCEPT_EXTRACTION_PROMPT.replace(
            "{source_text}",
            source_text,
        )

        return await self.generate(prompt=prompt)
