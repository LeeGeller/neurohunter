import asyncio
import uuid
from typing import (
    TypedDict,
)

from celery import (
    shared_task,
)
from sqlalchemy import (
    select,
)

from app.config.settings import (
    settings,
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


class HardConstraints(TypedDict):
    """Structured criteria for primary vacancy filtering."""

    salary: int | None
    experience_years: float | None
    education: str | None
    night_work_tolerance: str | None
    business_trip_tolerance: str | None
    work_formats: list[str]
    physical_activity_tolerance: str | None


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
            base_url=settings.ollama_host,
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
        hard_constraints = build_hard_constraints(user_profile)

        if not old_user_features:
            user_features = UserFeatures(
                **features,
                hard_constraints=hard_constraints,
            )
            session.add(user_features)
        else:
            old_user_features.job_titles = features["job_titles"]
            old_user_features.hard_constraints = hard_constraints
            old_user_features.preferences = features["preferences"]
            old_user_features.tolerances = features["tolerances"]
            old_user_features.context = features["context"]

        await session.commit()


def build_hard_constraints(profile: UserProfile) -> HardConstraints:
    """Build structured hard constraints for a user."""
    return {
        'salary': profile.salary,
        'experience_years': profile.experience_years,
        'education': profile.education,
        'night_work_tolerance': profile.night_work_tolerance,
        'business_trip_tolerance': profile.business_trip_tolerance,
        'work_formats': profile.preferred_work_formats or [],
        'physical_activity_tolerance': profile.physical_activity_tolerance,
    }
