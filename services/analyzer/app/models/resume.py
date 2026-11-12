"""Resume document models."""

import uuid
from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    ARRAY,
    UUID,
    Float,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import (
    JSONB,
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
    from app.models.professional_fit import (
        ProfessionalFit,
    )
    from app.models.user import (
        User,
    )


class ResumeDocument(Base):
    """User resume document model."""

    __tablename__ = "resume_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        unique=True,
        nullable=False,
    )

    user: Mapped['User'] = relationship(
        back_populates='resume',
        uselist=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


class ResumeFeatures(Base):
    """Resume features schema for vacancy matching."""

    __tablename__ = 'resume_features'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        primary_key=True,
    )

    user: Mapped['User'] = relationship(
        back_populates='resume_features',
    )

    professional_fit: Mapped['ProfessionalFit'] = relationship(
        back_populates='resume_feature',
        cascade='all, delete-orphan',
    )

    job_titles: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )

    hard_skills: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )

    soft_skills: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )

    experience: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    projects: Mapped[list[dict]] = mapped_column(
        JSONB,
        default=list,
    )

    weaknesses: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )

    strengths: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=list,
    )

    experience_resume: Mapped[list[dict]] = mapped_column(
        JSONB,
        default=list,
    )
