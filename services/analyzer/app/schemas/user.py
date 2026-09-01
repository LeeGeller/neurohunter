"""User profile schemas."""

import uuid
from datetime import (
    time,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.profile_enums import (
    AmbiguityTolerance,
    AutonomyLevel,
    BurnoutSensitivity,
    BusinessTripTolerance,
    ClientCommunicationTolerance,
    ConflictTolerance,
    ContextSwitchingTolerance,
    CustomerSupportTolerance,
    DeadlineTolerance,
    EducationLevel,
    FeedbackFrequencyPreference,
    InformationOverloadTolerance,
    InterruptionsTolerance,
    MeetingTolerance,
    MotivationFactor,
    MultitaskingTolerance,
    NightWorkTolerance,
    NoiseTolerance,
    OpenSpaceTolerance,
    OvertimeTolerance,
    PhoneCallTolerance,
    PhysicalActivityTolerance,
    PreferredManagementStyle,
    PreferredTaskStructure,
    PreferredTeamSize,
    PublicSpeakingTolerance,
    ShiftWorkTolerance,
    SocialOverloadSensitivity,
    StandingWorkTolerance,
    TaskVarietyPreference,
    TeamCommunicationTolerance,
    TravelTolerance,
    WeekendWork,
    WorkFormat,
)


class UserProfileCreate(BaseModel):
    """User profile schema.

    Info about the user, including personal details, preferences, and tolerances.
    User fills this form after registration.
    """

    age: int = Field(
        default=None,
        ge=14,
        le=100,
    )
    profession: str | None = None
    experience_years: float | None = None
    education: EducationLevel | None = None

    # Work preferences and tolerances
    preferred_work_days_per_week: int | None = Field(
        default=None,
        ge=1,
        le=7,
    )
    preferred_work_hours_per_day: float | None = Field(
        default=None,
        ge=1,
        le=24,
    )
    flexible_schedule_needed: bool | None = None
    overtime_tolerance: OvertimeTolerance | None = None
    preferred_end_time: time | None = None
    weekend_work: WeekendWork | None = None
    night_work_tolerance: NightWorkTolerance | None = None
    shift_work_tolerance: ShiftWorkTolerance | None = None
    business_trip_tolerance: BusinessTripTolerance | None = None

    # Communication preferences and tolerances
    client_communication_tolerance: ClientCommunicationTolerance | None = None
    team_communication_tolerance: TeamCommunicationTolerance | None = None
    meeting_tolerance: MeetingTolerance | None = None
    public_speaking_tolerance: PublicSpeakingTolerance | None = None
    phone_call_tolerance: PhoneCallTolerance | None = None
    customer_support_tolerance: CustomerSupportTolerance | None = None
    conflict_tolerance: ConflictTolerance | None = None

    # Task management preferences and tolerances
    multitasking_tolerance: MultitaskingTolerance | None = None
    deadline_tolerance: DeadlineTolerance | None = None
    context_switching_tolerance: ContextSwitchingTolerance | None = None
    ambiguity_tolerance: AmbiguityTolerance | None = None
    information_overload_tolerance: InformationOverloadTolerance | None = None
    interruptions_tolerance: InterruptionsTolerance | None = None

    # Stress management preferences and tolerances
    burnout_sensitivity: BurnoutSensitivity | None = None
    social_overload_sensitivity: SocialOverloadSensitivity | None = None
    preferred_team_size: PreferredTeamSize | None = None
    preferred_management_style: PreferredManagementStyle | None = None
    preferred_task_structure: PreferredTaskStructure | None = None
    task_variety_preference: TaskVarietyPreference | None = None
    autonomy_level: AutonomyLevel | None = None
    feedback_frequency_preference: FeedbackFrequencyPreference | None = None

    # Work environment preferences and tolerances
    noise_tolerance: NoiseTolerance | None = None
    open_space_tolerance: OpenSpaceTolerance | None = None

    # Work preferences
    preferred_work_formats: list[WorkFormat] = []

    # Work tolerancesW
    physical_activity_tolerance: PhysicalActivityTolerance | None = None
    standing_work_tolerance: StandingWorkTolerance | None = None
    travel_tolerance: TravelTolerance | None = None

    # Work factors
    motivation_factors: list[MotivationFactor] = []

    # Work importance

    income_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    stability_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    interesting_tasks_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    professional_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    horizontal_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    vertical_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    autonomy_level_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    flexible_schedule_needed_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    work_life_balance_importance: float | int = Field(
        default=None,
        ge=0,
        le=10,
    )
    remote_work_importance: float | int = Field(
        default=None,
        ge=0,
        le=10,
    )
    social_environment_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    recognition_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    meaningful_work_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    variety_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    creativity_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    dms_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    # Other information. For example, a short description of the user.
    about_me: str | None = None


class UserProfileRead(BaseModel):
    """User profile schema.

    Info about the user, including personal details, preferences, and tolerances.
    User fills this form after registration.
    """

    user_id: uuid.UUID

    age: int = Field(
        default=None,
        ge=14,
        le=100,
    )
    profession: str | None = None
    experience_years: float | None = None
    education: EducationLevel | None = None

    # Work preferences and tolerances
    preferred_work_days_per_week: int | None = Field(
        default=None,
        ge=1,
        le=7,
    )
    preferred_work_hours_per_day: float | None = Field(
        default=None,
        ge=1,
        le=24,
    )
    flexible_schedule_needed: bool | None = None
    overtime_tolerance: OvertimeTolerance | None = None
    preferred_end_time: time | None = None
    weekend_work: WeekendWork | None = None
    night_work_tolerance: NightWorkTolerance | None = None
    shift_work_tolerance: ShiftWorkTolerance | None = None
    business_trip_tolerance: BusinessTripTolerance | None = None

    # Communication preferences and tolerances
    client_communication_tolerance: ClientCommunicationTolerance | None = None
    team_communication_tolerance: TeamCommunicationTolerance | None = None
    meeting_tolerance: MeetingTolerance | None = None
    public_speaking_tolerance: PublicSpeakingTolerance | None = None
    phone_call_tolerance: PhoneCallTolerance | None = None
    customer_support_tolerance: CustomerSupportTolerance | None = None
    conflict_tolerance: ConflictTolerance | None = None

    # Task management preferences and tolerances
    multitasking_tolerance: MultitaskingTolerance | None = None
    deadline_tolerance: DeadlineTolerance | None = None
    context_switching_tolerance: ContextSwitchingTolerance | None = None
    ambiguity_tolerance: AmbiguityTolerance | None = None
    information_overload_tolerance: InformationOverloadTolerance | None = None
    interruptions_tolerance: InterruptionsTolerance | None = None

    # Stress management preferences and tolerances
    burnout_sensitivity: BurnoutSensitivity | None = None
    social_overload_sensitivity: SocialOverloadSensitivity | None = None
    preferred_team_size: PreferredTeamSize | None = None
    preferred_management_style: PreferredManagementStyle | None = None
    preferred_task_structure: PreferredTaskStructure | None = None
    task_variety_preference: TaskVarietyPreference | None = None
    autonomy_level: AutonomyLevel | None = None
    feedback_frequency_preference: FeedbackFrequencyPreference | None = None

    # Work environment preferences and tolerances
    noise_tolerance: NoiseTolerance | None = None
    open_space_tolerance: OpenSpaceTolerance | None = None

    # Work preferences
    preferred_work_formats: list[WorkFormat] = []

    # Work tolerancesW
    physical_activity_tolerance: PhysicalActivityTolerance | None = None
    standing_work_tolerance: StandingWorkTolerance | None = None
    travel_tolerance: TravelTolerance | None = None

    # Work factors
    motivation_factors: list[MotivationFactor] = []

    # Work importance

    income_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    stability_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    interesting_tasks_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    professional_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    horizontal_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    vertical_growth_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    autonomy_level_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    flexible_schedule_needed_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    work_life_balance_importance: float | int = Field(
        default=None,
        ge=0,
        le=10,
    )
    remote_work_importance: float | int = Field(
        default=None,
        ge=0,
        le=10,
    )
    social_environment_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    recognition_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    meaningful_work_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    variety_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    creativity_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )
    dms_importance: int | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    # Other information. For example, a short description of the user.
    about_me: str | None = None
