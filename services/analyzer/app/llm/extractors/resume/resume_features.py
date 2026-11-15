"""ResumeFeatures extractor using LLM."""

from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.prompts import (
    RESUME_FEATURES_PROMPT,
)
from app.schemas.user.resume_features import (
    ResumeFeaturesSchema,
)


class ResumeFeaturesExtractor(
    BaseExtractor[ResumeFeaturesSchema]
):
    """Analyze resumes using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
    ) -> None:
        """Initialize the ResumeFeaturesExtractor."""
        super().__init__(
            llm_client=llm_client,
            response_model=ResumeFeaturesSchema,
        )

    async def extract_features(self, resume: str) -> ResumeFeaturesSchema:
        """Extract structured features from a resume using LLM."""

        prompt = RESUME_FEATURES_PROMPT.format(
            resume_text=resume
        )

        return await self.generate(prompt=prompt)
