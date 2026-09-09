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
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import (
    Base,
)

if TYPE_CHECKING:
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

    job_titles = mapped_column(
        ARRAY(Text),
        default=list,
    )
    hard_skills = mapped_column(
        ARRAY(Text),
        default=list,
    )
    soft_skills = mapped_column(
        ARRAY(Text),
        default=list,
    )
    experience = mapped_column(
        Float,
        nullable=True,
    )
    projects = mapped_column(
        ARRAY(Text),
        default=list,
    )
    weaknesses = mapped_column(
        ARRAY(Text),
        default=list,
    )
    strengths = mapped_column(
        ARRAY(Text),
        default=list,
    )
    experience_resume = mapped_column(
        ARRAY(Text),
        default=list,
    )
