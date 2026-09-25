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
from app.llm.extractor import (
    ResumeFeaturesExtractor,
)
from app.models.resume import (
    ResumeDocument,
    ResumeFeatures,
)


@shared_task
def analyze_resume(user_id: uuid.UUID) -> None:

    asyncio.run(
        _analyze_resume(
            user_id=user_id,
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
        extractor = ResumeFeaturesExtractor(
            llm_client=llm_model,
        )

        new_features_resume = await extractor.extract_features(resume.text)

        old_resume_features_result = await session.execute(
            select(ResumeFeatures).where(
                ResumeFeatures.user_id == user_id,
            ),
        )
        old_resume_features = old_resume_features_result.scalar_one_or_none()

        if not old_resume_features:
            resume_features = ResumeFeatures(
                user_id=user_id,
                **new_features_resume,
            )
            session.add(resume_features)
        else:
            old_resume_features.job_titles = new_features_resume['job_titles']
            old_resume_features.hard_skills = new_features_resume['hard_skills']
            old_resume_features.soft_skills = new_features_resume['soft_skills']
            old_resume_features.experience = new_features_resume['experience']
            old_resume_features.projects = new_features_resume['projects']
            old_resume_features.weaknesses = new_features_resume['weaknesses']
            old_resume_features.strengths = new_features_resume['strengths']
            old_resume_features.experience_resume = new_features_resume['experience_resume']

        await session.commit()
