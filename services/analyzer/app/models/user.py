"""User database models."""

import uuid
from datetime import (
    time,
)

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import (
    ARRAY,
    UUID,
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
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
    ResumeDocument,
    ResumeFeatures,
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model."""

    __tablename__ = "users"

    profile: Mapped['UserProfile'] = relationship(
        back_populates='user',
        uselist=False,
    )

    user_features: Mapped['UserFeatures'] = relationship(
        back_populates='user',
        uselist=False,
    )

    resume: Mapped['ResumeDocument'] = relationship(
        back_populates='user',
        uselist=False,
    )

    resume_features: Mapped['ResumeFeatures'] = relationship(
        back_populates='user',
        uselist=False,
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


class UserProfile(Base):
    """User profile model.

    Info about the user, including personal details, preferences, and tolerances.
    User fills this form after registration.
    """

    __tablename__ = "user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        primary_key=True,
    )

    user: Mapped['User'] = relationship(
        back_populates='profile',
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    profession: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    experience_years: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    education: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Work preferences and tolerances

    preferred_work_days_per_week: Mapped[float | None] = mapped_column(
        Integer,
        nullable=True,
    )

    preferred_work_hours_per_day: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    flexible_schedule_needed: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    overtime_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    preferred_end_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    weekend_work: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    night_work_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    shift_work_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    business_trip_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Communication preferences and tolerances

    client_communication_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    team_communication_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    meeting_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    public_speaking_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    phone_call_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    customer_support_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    conflict_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Task management preferences and tolerances

    multitasking_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    deadline_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    context_switching_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    ambiguity_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    information_overload_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    interruptions_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Stress management preferences and tolerances

    burnout_sensitivity: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    social_overload_sensitivity: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    preferred_team_size: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    preferred_management_style: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    preferred_task_structure: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    task_variety_preference: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    autonomy_level: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    feedback_frequency_preference: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Work environment preferences and tolerances

    noise_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    open_space_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Work preferences

    preferred_work_formats: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    # Work tolerances

    physical_activity_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    standing_work_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    travel_tolerance: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Work factors

    motivation_factors: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    # Work importance

    income_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    stability_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    interesting_tasks_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    professional_growth_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    horizontal_growth_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    vertical_growth_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    autonomy_level_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    flexible_schedule_needed_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    work_life_balance_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    remote_work_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    social_environment_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    recognition_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    meaningful_work_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    variety_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    creativity_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    dms_importance: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Other information

    about_me: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
