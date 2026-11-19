"""ProfessionalFit model for match VacancyFeatures, ResumeFeatures."""


import uuid
from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    UUID,
    Boolean,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import (
    Base,
)

if TYPE_CHECKING:
    from app.models.resume import (
        ResumeFeatures,
    )
    from app.models.vacancy import (
        VacancyRequirements,
    )


class ProfessionalFit(Base):
    """Professional fit class."""

    __tablename__ = 'professional_fit'

    __table_args__ = (
        UniqueConstraint(
            'resume_id',
            'vacancy_requirements_id',
            name='uq_professional_fit_resume_id_vacancy_requirements_id',
        ),
    )

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
    mandatory_skills_coverage: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    mandatory_skill_groups_coverage: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    preferred_skills_coverage: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    preferred_skill_groups_coverage: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    # Experience
    low_experience: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    high_experience: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
