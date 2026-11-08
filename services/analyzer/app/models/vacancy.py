from typing import Optional
import uuid
from datetime import (
    datetime,
    time,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from sqlalchemy import (
    JSON,
    UUID,
    Boolean,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    String,
    Time,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import (
    Base,
)
from app.schemas.profile_enums import (
    AutonomyLevel,
    PreferredManagementStyle,
    PreferredTaskStructure,
    TaskVarietyPreference,
    WeekendWork,
)
from app.schemas.vacancy_enums import (
    VacancyFrequency,
    VacancyIntensity,
)


class Vacancy(BaseModel):
    """Vacancy model."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: str
    title: str
    vacancy_date: datetime = Field(alias='vacancydate')
    description: str
    company: str
    work_location: str | None = Field(alias='worklocation')
    work_format: str | None = Field(alias='workformat')
    salary_from: int | None = Field(alias='salaryfrom')
    salary_to: int | None = Field(alias='salaryto')
    currency: str | None
    url: str


class VacancyFeatures(Base):
    """Extract job vacancy attributes from the description."""

    __tablename__ = 'vacancy_features'

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    # Work schedule
    work_days_per_week: Mapped[float | None] = mapped_column(Float, nullable=True)
    work_hours_per_day: Mapped[float | None] = mapped_column(Float, nullable=True)
    weekly_work_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    work_schedule: Mapped[str | None] = mapped_column(String, nullable=True)
    flexible_schedule: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    # Overtime
    overtime_expected: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    overtime_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_overtime_frequency", native_enum=False),
        nullable=True,
    )

    # Work format
    work_format: Mapped[str | None] = mapped_column(String, nullable=True)
    remote_possible: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    office_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    hybrid_possible: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Work restrictions
    night_work: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_night_work", native_enum=False),
        nullable=True,
    )
    shift_work: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_shift_work", native_enum=False),
        nullable=True,
    )
    business_trips: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_business_trips", native_enum=False),
        nullable=True,
    )
    weekend_work: Mapped[WeekendWork | None] = mapped_column(
        SQLEnum(WeekendWork, name="vacancy_weekend_work", native_enum=False),
        nullable=True,
    )

    # Communication
    client_communication: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    team_communication: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    customer_facing: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    communication_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_communication_frequency", native_enum=False),
        nullable=True,
    )
    meeting_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_meeting_frequency", native_enum=False),
        nullable=True,
    )
    phone_calls_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    phone_calls_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_phone_calls_frequency", native_enum=False),
        nullable=True,
    )
    public_speaking_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    public_speaking_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_public_speaking_frequency", native_enum=False),
        nullable=True,
    )
    customer_support: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    conflict_level: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_conflict_level", native_enum=False),
        nullable=True,
    )

    # Workload and pressure
    multitasking_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    deadline_pressure: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_deadline_pressure", native_enum=False),
        nullable=True,
    )
    task_changes_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_task_changes_frequency", native_enum=False),
        nullable=True,
    )
    information_load: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_information_load", native_enum=False),
        nullable=True,
    )
    interruptions_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_interruptions_frequency", native_enum=False),
        nullable=True,
    )
    context_switching_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_context_switching_frequency", native_enum=False),
        nullable=True,
    )
    ambiguity_level: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_ambiguity_level", native_enum=False),
        nullable=True,
    )

    # Task structure
    task_clarity: Mapped[str | None] = mapped_column(String, nullable=True)
    task_predictability: Mapped[str | None] = mapped_column(String, nullable=True)
    task_independence: Mapped[str | None] = mapped_column(String, nullable=True)
    responsibility_level: Mapped[str | None] = mapped_column(String, nullable=True)
    task_structure: Mapped[PreferredTaskStructure | None] = mapped_column(
        SQLEnum(PreferredTaskStructure, name="vacancy_task_structure", native_enum=False),
        nullable=True,
    )
    task_variety: Mapped[TaskVarietyPreference | None] = mapped_column(
        SQLEnum(TaskVarietyPreference, name="vacancy_task_variety", native_enum=False),
        nullable=True,
    )

    # Work environment
    team_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    team_size_known: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    noise_level: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_noise_level", native_enum=False),
        nullable=True,
    )
    open_space: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    management_style: Mapped[PreferredManagementStyle | None] = mapped_column(
        SQLEnum(PreferredManagementStyle, name="vacancy_management_style", native_enum=False),
        nullable=True,
    )
    autonomy_level: Mapped[AutonomyLevel | None] = mapped_column(
        SQLEnum(AutonomyLevel, name="vacancy_autonomy_level", native_enum=False),
        nullable=True,
    )
    feedback_frequency: Mapped[VacancyFrequency | None] = mapped_column(
        SQLEnum(VacancyFrequency, name="vacancy_feedback_frequency", native_enum=False),
        nullable=True,
    )

    # Physical conditions
    physical_activity_level: Mapped[VacancyIntensity | None] = mapped_column(
        SQLEnum(VacancyIntensity, name="vacancy_physical_activity_level", native_enum=False),
        nullable=True,
    )
    standing_required: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Employment conditions
    employment_type: Mapped[str | None] = mapped_column(String, nullable=True)
    probation_period: Mapped[str | None] = mapped_column(String, nullable=True)
    salary_transparency: Mapped[str | None] = mapped_column(String, nullable=True)

    # Evidence extracted from the vacancy description
    evidence: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )


class VacancyRequirements(Base):
    """Vacancy requirements extracted from the description."""

    __tablename__ = 'vacancy_requirements'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('vacancy_features.vacancy_id'),
        unique=True,
        nullable=False,
    )

    # Skills
    mandatory_skills: Mapped[Optional[list[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    preferred_skills: Mapped[Optional[list[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )

    # Professional experience
    experience_min: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    experience_max: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # Education
    education_requirement: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # Evidence
    evidence: Mapped[Optional[list[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
