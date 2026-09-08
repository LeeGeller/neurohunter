"""Resume document models."""

import uuid

from sqlalchemy import (
    UUID,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import (
    Base,
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

    file_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
