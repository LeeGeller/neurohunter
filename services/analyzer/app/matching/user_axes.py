"""User axes for compatibility matrices."""

from typing import (
    Final,
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

# ---------------------------------------------------------------------------
# Ordered user axes
# ---------------------------------------------------------------------------

OVERTIME_AXIS: Final = (
    OvertimeTolerance.NEVER,
    OvertimeTolerance.RARELY,
    OvertimeTolerance.SOMETIMES,
    OvertimeTolerance.OFTEN,
    OvertimeTolerance.ALWAYS,
)


NIGHT_WORK_AXIS: Final = (
    NightWorkTolerance.NEVER,
    NightWorkTolerance.RARELY,
    NightWorkTolerance.SOMETIMES,
    NightWorkTolerance.OFTEN,
    NightWorkTolerance.ALWAYS,
)


SHIFT_WORK_AXIS: Final = (
    ShiftWorkTolerance.NEVER,
    ShiftWorkTolerance.LOW,
    ShiftWorkTolerance.MEDIUM,
    ShiftWorkTolerance.HIGH,
)


BUSINESS_TRIP_AXIS: Final = (
    BusinessTripTolerance.NEVER,
    BusinessTripTolerance.LOW,
    BusinessTripTolerance.MEDIUM,
    BusinessTripTolerance.HIGH,
)


CLIENT_COMMUNICATION_AXIS: Final = (
    ClientCommunicationTolerance.NEVER,
    ClientCommunicationTolerance.LOW_CLIENTS,
    ClientCommunicationTolerance.RARE__CLIENTS,
    ClientCommunicationTolerance.MEDIUM_CLIENTS,
    ClientCommunicationTolerance.HIGH_CLIENTS,
)


TEAM_COMMUNICATION_AXIS: Final = (
    TeamCommunicationTolerance.NEVER,
    TeamCommunicationTolerance.LOW_TEAM,
    TeamCommunicationTolerance.RARE_TEAM,
    TeamCommunicationTolerance.MEDIUM_TEAM,
    TeamCommunicationTolerance.HIGH_TEAM,
)


MEETING_AXIS: Final = (
    MeetingTolerance.NEVER,
    MeetingTolerance.LOW_MEETINGS,
    MeetingTolerance.MEDIUM_MEETINGS,
    MeetingTolerance.HIGH_MEETINGS,
)


PUBLIC_SPEAKING_AXIS: Final = (
    PublicSpeakingTolerance.NEVER,
    PublicSpeakingTolerance.LOW_PUBLIC_SPEAKING,
    PublicSpeakingTolerance.MEDIUM_PUBLIC_SPEAKING,
    PublicSpeakingTolerance.HIGH_PUBLIC_SPEAKING,
)


PHONE_CALL_AXIS: Final = (
    PhoneCallTolerance.NEVER,
    PhoneCallTolerance.COLD_CALLS_TRADER,
    PhoneCallTolerance.COLD_CALLS,
    PhoneCallTolerance.WARM_CALLS_TRADER,
    PhoneCallTolerance.WARM_CALLS,
    PhoneCallTolerance.HOT_CALLS_TRADER,
    PhoneCallTolerance.HOT_CALLS,
)


CUSTOMER_SUPPORT_AXIS: Final = (
    CustomerSupportTolerance.NOT_ACCEPTABLE,
    CustomerSupportTolerance.DIFFICULT,
    CustomerSupportTolerance.NEUTRAL,
    CustomerSupportTolerance.ACCEPTABLE,
    CustomerSupportTolerance.PREFERRED,
)


CONFLICT_AXIS: Final = (
    ConflictTolerance.AVOID,
    ConflictTolerance.LOW,
    ConflictTolerance.MEDIUM,
    ConflictTolerance.HIGH,
)


MULTITASKING_AXIS: Final = (
    MultitaskingTolerance.SINGLE_TASK,
    MultitaskingTolerance.FEW_TASKS,
    MultitaskingTolerance.MANY_TASKS,
)


DEADLINE_AXIS: Final = (
    DeadlineTolerance.NEVER,
    DeadlineTolerance.LOW,
    DeadlineTolerance.MEDIUM,
    DeadlineTolerance.HIGH,
)


CONTEXT_SWITCHING_AXIS: Final = (
    ContextSwitchingTolerance.MINIMAL,
    ContextSwitchingTolerance.OCCASIONAL,
    ContextSwitchingTolerance.FREQUENT,
)


AMBIGUITY_AXIS: Final = (
    AmbiguityTolerance.AVOID,
    AmbiguityTolerance.LOW,
    AmbiguityTolerance.MEDIUM,
    AmbiguityTolerance.HIGH,
    AmbiguityTolerance.VERY_HIGH,
)


INFORMATION_OVERLOAD_AXIS: Final = (
    InformationOverloadTolerance.AVOID,
    InformationOverloadTolerance.LOW,
    InformationOverloadTolerance.MEDIUM,
    InformationOverloadTolerance.HIGH,
)


INTERRUPTIONS_AXIS: Final = (
    InterruptionsTolerance.AVOID,
    InterruptionsTolerance.LOW,
    InterruptionsTolerance.MEDIUM,
    InterruptionsTolerance.HIGH,
)


BURNOUT_SENSITIVITY_AXIS: Final = (
    BurnoutSensitivity.LOW,
    BurnoutSensitivity.MEDIUM,
    BurnoutSensitivity.HIGH,
)


SOCIAL_OVERLOAD_SENSITIVITY_AXIS: Final = (
    SocialOverloadSensitivity.LOW,
    SocialOverloadSensitivity.MEDIUM,
    SocialOverloadSensitivity.HIGH,
)


PREFERRED_TEAM_SIZE_AXIS: Final = (
    PreferredTeamSize.SOLO,
    PreferredTeamSize.SMALL,
    PreferredTeamSize.MEDIUM,
    PreferredTeamSize.LARGE,
)


PREFERRED_TASK_STRUCTURE_AXIS: Final = (
    PreferredTaskStructure.HIGHLY_STRUCTURED,
    PreferredTaskStructure.STRUCTURED,
    PreferredTaskStructure.BALANCED,
    PreferredTaskStructure.FLEXIBLE,
    PreferredTaskStructure.OPEN_ENDED,
)


TASK_VARIETY_AXIS: Final = (
    TaskVarietyPreference.REPETITIVE,
    TaskVarietyPreference.MOSTLY_REPETITIVE,
    TaskVarietyPreference.BALANCED,
    TaskVarietyPreference.MOSTLY_DIVERSE,
    TaskVarietyPreference.HIGHLY_DIVERSE,
)


AUTONOMY_AXIS: Final = (
    AutonomyLevel.LOW,
    AutonomyLevel.MEDIUM,
    AutonomyLevel.HIGH,
)


FEEDBACK_FREQUENCY_AXIS: Final = (
    FeedbackFrequencyPreference.AS_NEEDED,
    FeedbackFrequencyPreference.OCCASIONAL,
    FeedbackFrequencyPreference.REGULAR,
    FeedbackFrequencyPreference.FREQUENT,
)


NOISE_AXIS: Final = (
    NoiseTolerance.VERY_LOW,
    NoiseTolerance.LOW,
    NoiseTolerance.MEDIUM,
    NoiseTolerance.HIGH,
)


OPEN_SPACE_AXIS: Final = (
    OpenSpaceTolerance.VERY_LOW,
    OpenSpaceTolerance.LOW,
    OpenSpaceTolerance.MEDIUM,
    OpenSpaceTolerance.HIGH,
)


PHYSICAL_ACTIVITY_AXIS: Final = (
    PhysicalActivityTolerance.NEVER,
    PhysicalActivityTolerance.LOW,
    PhysicalActivityTolerance.MEDIUM,
    PhysicalActivityTolerance.HIGH,
)


STANDING_WORK_AXIS: Final = (
    StandingWorkTolerance.LOW,
    StandingWorkTolerance.MEDIUM,
    StandingWorkTolerance.HIGH,
)


TRAVEL_AXIS: Final = (
    TravelTolerance.NEVER,
    TravelTolerance.LOW,
    TravelTolerance.MEDIUM,
    TravelTolerance.HIGH,
)


# ---------------------------------------------------------------------------
# Categorical user axes
# ---------------------------------------------------------------------------

EDUCATION_AXIS: Final = (
    EducationLevel.SECONDARY_EDUCATION,
    EducationLevel.SPECIAL_EDUCATION,
    EducationLevel.INCOMPLETE_HIGHER_EDUCATION,
    EducationLevel.STUDENT_SPECIAL_EDUCATION,
    EducationLevel.STUDENT_HIGHTER_EDUCATION,
    EducationLevel.HIGHTER_EDUCATION,
)


WEEKEND_WORK_AXIS: Final = (
    WeekendWork.USUALLY_WEEKENDS,
    WeekendWork.FLEXIBLE_DAYS_OFF,
    WeekendWork.WEEKENDS_ON_WEEKDAYS,
)


WORK_FORMAT_AXIS: Final = (
    WorkFormat.REMOTE,
    WorkFormat.HYBRID,
    WorkFormat.OFFICE,
)


MANAGEMENT_STYLE_AXIS: Final = (
    PreferredManagementStyle.STRUCTURED,
    PreferredManagementStyle.SUPPORTIVE,
    PreferredManagementStyle.AUTONOMOUS,
    PreferredManagementStyle.COLLABORATIVE,
    PreferredManagementStyle.DIRECT,
    PreferredManagementStyle.FLEXIBLE,
)


# ---------------------------------------------------------------------------
# User axes registry
# ---------------------------------------------------------------------------

USER_AXES: Final = {
    'overtime': OVERTIME_AXIS,
    'night_work': NIGHT_WORK_AXIS,
    'shift_work': SHIFT_WORK_AXIS,
    'business_trip': BUSINESS_TRIP_AXIS,
    'client_communication': CLIENT_COMMUNICATION_AXIS,
    'team_communication': TEAM_COMMUNICATION_AXIS,
    'meetings': MEETING_AXIS,
    'public_speaking': PUBLIC_SPEAKING_AXIS,
    'phone_calls': PHONE_CALL_AXIS,
    'customer_support': CUSTOMER_SUPPORT_AXIS,
    'conflict': CONFLICT_AXIS,
    'multitasking': MULTITASKING_AXIS,
    'deadlines': DEADLINE_AXIS,
    'context_switching': CONTEXT_SWITCHING_AXIS,
    'ambiguity': AMBIGUITY_AXIS,
    'information_overload': INFORMATION_OVERLOAD_AXIS,
    'interruptions': INTERRUPTIONS_AXIS,
    'burnout_sensitivity': BURNOUT_SENSITIVITY_AXIS,
    'social_overload_sensitivity': SOCIAL_OVERLOAD_SENSITIVITY_AXIS,
    'team_size': PREFERRED_TEAM_SIZE_AXIS,
    'task_structure': PREFERRED_TASK_STRUCTURE_AXIS,
    'task_variety': TASK_VARIETY_AXIS,
    'autonomy': AUTONOMY_AXIS,
    'feedback_frequency': FEEDBACK_FREQUENCY_AXIS,
    'noise': NOISE_AXIS,
    'open_space': OPEN_SPACE_AXIS,
    'physical_activity': PHYSICAL_ACTIVITY_AXIS,
    'standing_work': STANDING_WORK_AXIS,
    'travel': TRAVEL_AXIS,
    'education': EDUCATION_AXIS,
    'weekend_work': WEEKEND_WORK_AXIS,
    'work_format': WORK_FORMAT_AXIS,
    'management_style': MANAGEMENT_STYLE_AXIS,
}
