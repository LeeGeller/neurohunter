"""ProfessionalFit model for match VacancyFeatures, ResumeFeatures."""


import uuid

from sqlalchemy import (
    ARRAY,
    UUID,
    Float,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import (
    Base,
)
from app.models.resume import (
    ResumeFeatures,
)
from app.models.vacancy import (
    VacancyRequirements,
)


class ProfessionalFit(Base):
    """Professional fit class."""

    __tablename__ = 'professional_fit'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('resume_features.user_id'),
        nullable=False,
    )

    resume_feature: Mapped['ResumeFeatures'] = relationship(
        back_populates='professional_fit'
    )

    vacancy_requirements_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('vacancy_requirements.id'),
        nullable=False,
    )

    vacancy_requirements: Mapped['VacancyRequirements'] = relationship(
        back_populates='professional_fit'
    )

    # Semantic link
    hard_skills: Mapped[list[str]]
