"""Vacancy features schema."""
from datetime import (
    time,
)
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.schemas.user.profile_enums import (
    AutonomyLevel,
    PreferredManagementStyle,
    PreferredTaskStructure,
    TaskVarietyPreference,
    WeekendWork,
)
from app.schemas.vacancy.vacancy_enums import (
    VacancyFrequency,
    VacancyIntensity,
)


class VacancyFeaturesSchema(BaseModel):
    """Vacancy features extracted for LLM."""

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
)

    # Work schedule
    work_days_per_week: Optional[float] = Field(
        alias='workDaysPerWeek',
    )
    work_hours_per_day: Optional[float] = Field(
        alias='workHoursPerDay',
    )
    weekly_work_hours: Optional[float] = Field(
        alias='weeklyWorkHours',
    )
    work_schedule: Optional[str] = Field(
        alias='workSchedule',
    )
    flexible_schedule: Optional[bool] = Field(
        alias='flexibleSchedule',
    )
    start_time: Optional[time] = Field(
        alias='startTime',
    )
    end_time: Optional[time] = Field(
        alias='endTime',
    )

    # Overtime
    overtime_expected: Optional[bool] = Field(
        alias='overtimeExpected',
    )
    overtime_frequency: Optional[VacancyFrequency] = Field(
        alias='overtimeFrequency',
    )

    # Work format
    work_format: Optional[str] = Field(
        alias='workFormat',
    )
    remote_possible: Optional[bool] = Field(
        alias='remotePossible',
    )
    office_required: Optional[bool] = Field(
        alias='officeRequired',
    )
    hybrid_possible: Optional[bool] = Field(
        alias='hybridPossible',
    )

    # Work restrictions
    night_work: Optional[VacancyFrequency] = Field(
        alias='nightWork',
    )
    shift_work: Optional[VacancyFrequency] = Field(
        alias='shiftWork',
    )
    business_trips: Optional[VacancyFrequency] = Field(
        alias='businessTrips',
    )
    weekend_work: Optional[WeekendWork] = Field(
        alias='weekendWork',
    )

    # Communication
    client_communication: Optional[bool] = Field(
        alias='clientCommunication',
    )
    team_communication: Optional[bool] = Field(
        alias='teamCommunication',
    )
    customer_facing: Optional[bool] = Field(
        alias='customerFacing',
    )
    communication_frequency: Optional[VacancyFrequency] = Field(
        alias='communicationFrequency',
    )
    meeting_frequency: Optional[VacancyFrequency] = Field(
        alias='meetingFrequency',
    )
    phone_calls_required: Optional[bool] = Field(
        alias='phoneCallsRequired',
    )
    phone_calls_frequency: Optional[VacancyFrequency] = Field(
        alias='phoneCallsFrequency',
    )
    public_speaking_required: Optional[bool] = Field(
        alias='publicSpeakingRequired',
    )
    public_speaking_frequency: Optional[VacancyFrequency] = Field(
        alias='publicSpeakingFrequency',
    )
    customer_support: Optional[bool] = Field(
        alias='customerSupport',
    )
    conflict_level: Optional[VacancyIntensity] = Field(
        alias='conflictLevel',
    )

    # Workload and pressure
    multitasking_required: Optional[bool] = Field(
        alias='multitaskingRequired',
    )
    deadline_pressure: Optional[VacancyIntensity] = Field(
        alias='deadlinePressure',
    )
    task_changes_frequency: Optional[VacancyFrequency] = Field(
        alias='taskChangesFrequency',
    )
    information_load: Optional[VacancyIntensity] = Field(
        alias='informationLoad',
    )
    interruptions_frequency: Optional[VacancyFrequency] = Field(
        alias='interruptionsFrequency',
    )
    context_switching_frequency: Optional[VacancyFrequency] = Field(
        alias='contextSwitchingFrequency',
    )
    ambiguity_level: Optional[VacancyIntensity] = Field(
        alias='ambiguityLevel',
    )

    # Task structure
    task_clarity: Optional[str] = Field(
        alias='taskClarity',
    )
    task_predictability: Optional[str] = Field(
        alias='taskPredictability',
    )
    task_independence: Optional[str] = Field(
        alias='taskIndependence',
    )
    responsibility_level: Optional[str] = Field(
        alias='responsibilityLevel',
    )
    task_structure: Optional[PreferredTaskStructure] = Field(
        alias='taskStructure',
    )
    task_variety: Optional[TaskVarietyPreference] = Field(
        alias='taskVariety',
    )

    # Work environment
    team_size: Optional[int] = Field(
        alias='teamSize',
    )
    team_size_known: Optional[bool] = Field(
        alias='teamSizeKnown',
    )
    noise_level: Optional[VacancyIntensity] = Field(
        alias='noiseLevel',
    )
    open_space: Optional[bool] = Field(
        alias='openSpace',
    )
    management_style: Optional[PreferredManagementStyle] = Field(
        alias='managementStyle',
    )
    autonomy_level: Optional[AutonomyLevel] = Field(
        alias='autonomyLevel',
    )
    feedback_frequency: Optional[VacancyFrequency] = Field(
        alias='feedbackFrequency',
    )

    # Physical conditions
    physical_activity_level: Optional[VacancyIntensity] = Field(
        alias='physicalActivityLevel',
    )
    standing_required: Optional[bool] = Field(
        alias='standingRequired',
    )

    # Employment conditions
    employment_type: Optional[str] = Field(
        alias='employmentType',
    )
    probation_period: Optional[str] = Field(
        alias='probationPeriod',
    )
    salary_transparency: Optional[str] = Field(
        alias='salaryTransparency',
    )

    # Evidence extracted from the vacancy description
    evidence: list[str] = Field(
        default_factory=list,
    )
