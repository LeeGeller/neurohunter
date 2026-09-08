"""Features models for LLM."""
import uuid

from sqlalchemy import (
    ARRAY,
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


class UserFeatures(Base):
    """User features schema for vacancy matching."""

    __tablename__ = 'user_features'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        primary_key=True,
    )
    user: Mapped['User'] = relationship(
        back_populates='user_features',
    )


    # Parameters used for vacancy matching
    hard_constraints: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )
    preferences: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )
    tolerances: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    # Additional context for LLM to better understand the user
    context: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )
