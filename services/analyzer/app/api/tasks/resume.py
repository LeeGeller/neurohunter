import asyncio
import uuid

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
from app.llm.extractors.knowledge.concept_extraction import (
    ConceptExtractor,
)
from app.llm.extractors.resume.resume_features import (
    ResumeFeaturesExtractor,
)
from app.models.resume import (
    ResumeDocument,
    ResumeFeatures,
)


@shared_task
def analyze_resume(user_id: str) -> None:
    """Start Celery task."""

    asyncio.run(
        _analyze_resume(
            user_id=uuid.UUID(user_id),
        ),
    )


async def _analyze_resume(user_id: uuid.UUID) -> None:
    """Analyze user resume using LLM."""

    async for session in get_session():
        result = await session.execute(
            select(ResumeDocument).where(
                ResumeDocument.user_id == user_id,
            ),
        )

        resume = result.scalar_one_or_none()

        if not resume:
            raise ValueError(f'Не найден резюме для пользоватея: {user_id}')

        llm_model = OllamaClient(
            base_url=settings.ollama_host,
            model=settings.ollama_model
        )
        try:
            concept_extractor = ConceptExtractor(
                llm_client=llm_model,
            )

            extractor = ResumeFeaturesExtractor(
                llm_client=llm_model,
                concept_extractor=concept_extractor,
            )

            new_features_resume = await extractor.extract_features(
                resume.text,
                )
        finally:
            await llm_model.close()

        old_resume_features_result = await session.execute(
            select(ResumeFeatures).where(
                ResumeFeatures.user_id == user_id,
            ),
        )
        old_resume_features = old_resume_features_result.scalar_one_or_none()

        new_features_resume_data = new_features_resume.model_dump()

        if not old_resume_features:
            resume_features = ResumeFeatures(
                user_id=user_id,
                **new_features_resume_data,
            )

            session.add(resume_features)
        else:
            for field, value in new_features_resume_data.items():
                setattr(
                    old_resume_features,
                    field,
                    value,
                )

        await session.commit()
