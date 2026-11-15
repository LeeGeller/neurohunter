from typing import (
    Optional,
)

from app.llm.client import (
    OllamaClient,
)
from app.llm.prompts import (
    RESUME_FEATURES_PROMPT,
)
from app.schemas.user.resume_features import (
    ResumeFeaturesSchema,
)


class ResumeFeaturesExtractor:
    """Analyze resumes using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_schema: Optional[dict] = None,
    ) -> None:
        """Initialize the ResumeFeaturesExtractor."""
        self.llm_client = llm_client
        self.response_schema = response_schema

    async def extract_features(self, resume: str) -> ResumeFeaturesSchema:
        """Extract structured features from a resume using LLM."""

        prompt = RESUME_FEATURES_PROMPT.format(
            resume_text=resume
        )

        response = await self.llm_client.generate(
            prompt,
            self.response_schema,
        )

        resume_features = ResumeFeaturesSchema.model_validate_json(response)

        return resume_features
