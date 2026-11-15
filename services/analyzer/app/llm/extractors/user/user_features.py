"""UserFeatures extraxtor using LLM."""

from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.prompts import (
    USER_FEATURES_PROMPT,
)
from app.models.user import (
    UserProfile,
)
from app.schemas.user.user_features import (
    UserFeaturesSchema,
)


class UserFeaturesExtractor(
    BaseExtractor[UserFeaturesSchema]
):
    """Analyze users using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        super().__init__(
            llm_client=llm_client,
            response_model=UserFeaturesSchema
        )

    async def extract_features(self, user: UserProfile) -> UserFeaturesSchema:
        """Extract structured features from a user using LLM."""

        profile_dict = self.profile_to_dict(user)
        prompt = USER_FEATURES_PROMPT.format(**profile_dict)

        return await self.generate(prompt=prompt)

    @staticmethod
    def profile_to_dict(
        user: UserProfile,
    ) -> dict:
        """Convert UserProfile object to dictionary."""
        return {
            column.name: getattr(user, column.name)
            for column in user.__table__.columns
            if column.name != 'user_id'
        }
