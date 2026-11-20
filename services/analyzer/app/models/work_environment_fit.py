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
    from app.models.user import (
        UserProfile,
    )
    from app.models.vacancy import (
        VacancyFeatures,
    )


class WorkEnvironmentFit(Base):
    """Mapper for UserProfile and VacancyFeature."""

    __tablename__ = 'work_environment_fit'

    __table__args__ = (
        UniqueConstraint(
            'profile_id',
            'vacancy_features_id',
            name='uq_work_environment_fit_profile_vacancy',
        )
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_profiles.user_id'),
        nullable=False,
    )
    profile: Mapped['UserProfile'] = relationship(
        back_populates='work_environment_fit',
    )

    vacancy_features_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('vacancy_features.vacancy_id'),
        nullable=False,
    )
    vacancy_features: Mapped['VacancyFeatures'] = relationship(
        back_populates='work_environment_fit',
    )
