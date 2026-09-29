from datetime import (
    datetime,
    time,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class Vacancy(BaseModel):
    """Vacancy model."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

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

    """Extract job vacancy attributes from the description."""

    vacancy_id: str

    # Work schedule

    work_days_per_week: float | None = None
    work_hours_per_day: float | None = None
    weekly_work_hours: float | None = None
    work_schedule: str | None = None
    flexible_schedule: bool | None = None
    start_time: time | None = None
    end_time: time | None = None

    # Overtime

    overtime_expected: bool | None = None
    overtime_frequency: str | None = None

    # Work format

    work_format: str | None = None
    remote_possible: bool | None = None
    office_required: bool | None = None
    hybrid_possible: bool | None = None

    # Work restrictions

    night_work: str | None = None
    shift_work: str | None = None
    business_trips: str | None = None
    weekend_work: str | None = None

    # Communication

    client_communication: bool | None = None
    team_communication: bool | None = None
    customer_facing: bool | None = None
    communication_frequency: str | None = None
    meeting_frequency: str | None = None
    phone_calls_required: bool | None = None
    phone_calls_frequency: str | None = None
    public_speaking_required: bool | None = None
    public_speaking_frequency: str | None = None
    customer_support: bool | None = None
    conflict_level: str | None = None

    # Workload and pressure

    multitasking_required: bool | None = None
    deadline_pressure: str | None = None
    task_changes_frequency: str | None = None
    information_load: str | None = None
    interruptions_frequency: str | None = None
    context_switching_frequency: str | None = None
    ambiguity_level: str | None = None

    # Task structure

    task_clarity: str | None = None
    task_predictability: str | None = None
    task_independence: str | None = None
    responsibility_level: str | None = None
    task_structure: str | None = None
    task_variety: str | None = None

    # Work environment

    team_size: int | None = None
    team_size_known: bool | None = None
    noise_level: str | None = None
    open_space: bool | None = None
    management_style: str | None = None
    autonomy_level: str | None = None
    feedback_frequency: str | None = None

    # Physical conditions

    physical_activity_level: str | None = None
    standing_required: bool | None = None

    # Employment conditions

    employment_type: str | None = None
    probation_period: str | None = None
    salary_transparency: str | None = None

    # Evidence extracted from the vacancy description

    evidence: list[str] = []


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
