import json

from app.llm.client import (
    OllamaClient,
)
from app.llm.prompts import (
    USER_FEATURES_PROMPT,
)
from app.models.user import (
    UserProfile,
)


class UserFeaturesExtractor:
    """Analyze users using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_features(self, user: UserProfile) -> dict:
        """Extract structured features from a user using LLM."""

        profile_dict = self.profile_to_dict(user)
        prompt = USER_FEATURES_PROMPT.format(**profile_dict)

        response = await self.llm_client.generate(prompt)

        return json.loads(response)

    def profile_to_dict(self, user: UserProfile) -> dict:
        """Convert UserProfile object to dictionary."""
        return {
            column.name: getattr(user, column.name)
            for column in user.__table__.columns
        }
