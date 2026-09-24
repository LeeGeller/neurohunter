import asyncio
import uuid

from celery import (
    shared_task,
)
from sqlalchemy import (
    select,
)

from app.database.postgres import (
    get_session,
)
from app.llm.client import (
    OllamaClient,
)
from app.llm.extractor import (
    UserFeaturesExtractor,
)
from app.models.user import (
    UserFeatures,
    UserProfile,
)
from app.config.settings import (
    settings,
)


@shared_task
def analyze_user_profile(user_id: uuid.UUID) -> None:

    asyncio.run(
        _analyze_user_profile(
            user_id=user_id,
        ),
    )


async def _analyze_user_profile(user_id: uuid.UUID) -> None:
    """Analyze user profile using LLM."""
    async for session in get_session():
        result = await session.execute(
            select(UserProfile).where(
                UserProfile.user_id == user_id,
            ),
        )

        user_profile = result.scalar_one_or_none()

        if not user_profile:
            raise ValueError(f'Не найден профиль для пользоватея: {user_id}')

        llm_model = OllamaClient(
            base_url=settings.ollama_url,
            model=settings.ollama_model
        )
        extractor = UserFeaturesExtractor(
            llm_client=llm_model,
        )

        features = await extractor.extract_features(user_profile)

        old_user_features_result = await session.execute(
            select(UserFeatures).where(
                UserFeatures.user_id == user_id,
            ),
        )
        old_user_features = old_user_features_result.scalar_one_or_none()

        if not old_user_features:
            user_features = UserFeatures(
                user_id=user_id,
                **features,
            )
            session.add(user_features)
        else:
            old_user_features.hard_constraints = features['hard_constraints']
            old_user_features.preferences = features['preferences']
            old_user_features.tolerances = features['tolerances']
            old_user_features.context = features['context']

        await session.commit()
