from datetime import datetime

from pydantic import BaseModel, Field


class Vacancy(BaseModel):
    """Vacancy model."""

    id: str
    title: str
    vacancy_date: datetime = Field(alias="vacancydate")
    description: str
    company: str
    work_location: str | None = Field(alias="worklocation")
    work_format: str | None = Field(alias="workformat")
    salary_from: int | None = Field(alias="salaryfrom")
    salary_to: int | None = Field(alias="salaryto")
    currency: str | None
    url: str


class VacancyFeatures(BaseModel):
    """Extracts job vacancy attributes from the
    description and work format.
    """

    vacancy_id: str

    # Work schedule
    work_days_per_week: float | None
    work_hours_per_day: float | None
    weekly_work_hours: float | None
    work_schedule: str | None
    flexible_schedule: bool | None

    # Overtime
    overtime_expected: bool | None
    overtime_frequency: str | None

    # Work format
    work_format: str | None
    remote_possible: bool | None
    office_required: bool | None
    hybrid_possible: bool | None

    # Communication
    client_communication: bool | None
    team_communication: bool | None
    customer_facing: bool | None
    communication_frequency: str | None
    meeting_frequency: str | None

    # Workload and pressure
    multitasking_required: bool | None
    deadline_pressure: str | None
    task_changes_frequency: str | None

    # Task structure
    task_clarity: str | None
    task_predictability: str | None
    task_independence: str | None
    responsibility_level: str | None

    # Work environment
    team_size: int | None
    management_style: str | None

    # Employment conditions
    employment_type: str | None
    probation_period: str | None
    salary_transparency: str | None

    # Evidence extracted from the vacancy description
    evidence: list[str]


class VacancyMatch(BaseModel):
    """Personalized vacancy match for a user."""

    vacancy_id: str
    user_id: str

    # Overall profile match
    profile_match: float

    # Professional skills match
    skills_match: float

    # Experience match
    experience_match: float

    # Work format match
    work_format_match: float

    # Personal burnout risk
    burnout_risk: float

    # Personal workload risk
    workload_risk: float

    # Personal social overload risk
    social_overload_risk: float

    # Why the vacancy is a good/bad fit
    explanation: str
