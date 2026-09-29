"""Vacancy axes for compatibility matrices."""

from typing import (
    Final,
)

from app.schemas.profile_enums import (
    AmbiguityTolerance,
    AutonomyLevel,
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
    StandingWorkTolerance,
    TaskVarietyPreference,
    TeamCommunicationTolerance,
    TravelTolerance,
    WeekendWork,
    WorkFormat,
)

VACANCY_OVERTIME_AXIS: Final = (
    OvertimeTolerance.NEVER,
    OvertimeTolerance.RARELY,
    OvertimeTolerance.SOMETIMES,
    OvertimeTolerance.OFTEN,
    OvertimeTolerance.ALWAYS,
)


VACANCY_NIGHT_WORK_AXIS: Final = (
    NightWorkTolerance.NEVER,
    NightWorkTolerance.RARELY,
    NightWorkTolerance.SOMETIMES,
    NightWorkTolerance.OFTEN,
    NightWorkTolerance.ALWAYS,
)


VACANCY_SHIFT_WORK_AXIS: Final = (
    ShiftWorkTolerance.NEVER,
    ShiftWorkTolerance.LOW,
    ShiftWorkTolerance.MEDIUM,
    ShiftWorkTolerance.HIGH,
)


VACANCY_BUSINESS_TRIP_AXIS: Final = (
    BusinessTripTolerance.NEVER,
    BusinessTripTolerance.LOW,
    BusinessTripTolerance.MEDIUM,
    BusinessTripTolerance.HIGH,
)


VACANCY_CLIENT_COMMUNICATION_AXIS: Final = (
    ClientCommunicationTolerance.NEVER,
    ClientCommunicationTolerance.LOW_CLIENTS,
    ClientCommunicationTolerance.RARE__CLIENTS,
    ClientCommunicationTolerance.MEDIUM_CLIENTS,
    ClientCommunicationTolerance.HIGH_CLIENTS,
)


VACANCY_TEAM_COMMUNICATION_AXIS: Final = (
    TeamCommunicationTolerance.NEVER,
    TeamCommunicationTolerance.LOW_TEAM,
    TeamCommunicationTolerance.RARE_TEAM,
    TeamCommunicationTolerance.MEDIUM_TEAM,
    TeamCommunicationTolerance.HIGH_TEAM,
)


VACANCY_MEETING_AXIS: Final = (
    MeetingTolerance.NEVER,
    MeetingTolerance.LOW_MEETINGS,
    MeetingTolerance.MEDIUM_MEETINGS,
    MeetingTolerance.HIGH_MEETINGS,
)


VACANCY_PUBLIC_SPEAKING_AXIS: Final = (
    PublicSpeakingTolerance.NEVER,
    PublicSpeakingTolerance.LOW_PUBLIC_SPEAKING,
    PublicSpeakingTolerance.MEDIUM_PUBLIC_SPEAKING,
    PublicSpeakingTolerance.HIGH_PUBLIC_SPEAKING,
)


VACANCY_PHONE_CALL_AXIS: Final = (
    PhoneCallTolerance.NEVER,
    PhoneCallTolerance.COLD_CALLS,
    PhoneCallTolerance.WARM_CALLS,
    PhoneCallTolerance.HOT_CALLS,
)


VACANCY_CUSTOMER_SUPPORT_AXIS: Final = (
    CustomerSupportTolerance.NOT_ACCEPTABLE,
    CustomerSupportTolerance.DIFFICULT,
    CustomerSupportTolerance.NEUTRAL,
    CustomerSupportTolerance.ACCEPTABLE,
    CustomerSupportTolerance.PREFERRED,
)


VACANCY_CONFLICT_AXIS: Final = (
    ConflictTolerance.AVOID,
    ConflictTolerance.LOW,
    ConflictTolerance.MEDIUM,
    ConflictTolerance.HIGH,
)


VACANCY_MULTITASKING_AXIS: Final = (
    MultitaskingTolerance.SINGLE_TASK,
    MultitaskingTolerance.FEW_TASKS,
    MultitaskingTolerance.MANY_TASKS,
)


VACANCY_DEADLINE_AXIS: Final = (
    DeadlineTolerance.NEVER,
    DeadlineTolerance.LOW,
    DeadlineTolerance.MEDIUM,
    DeadlineTolerance.HIGH,
)


VACANCY_CONTEXT_SWITCHING_AXIS: Final = (
    ContextSwitchingTolerance.MINIMAL,
    ContextSwitchingTolerance.OCCASIONAL,
    ContextSwitchingTolerance.FREQUENT,
)


VACANCY_AMBIGUITY_AXIS: Final = (
    AmbiguityTolerance.AVOID,
    AmbiguityTolerance.LOW,
    AmbiguityTolerance.MEDIUM,
    AmbiguityTolerance.HIGH,
    AmbiguityTolerance.VERY_HIGH,
)


VACANCY_INFORMATION_OVERLOAD_AXIS: Final = (
    InformationOverloadTolerance.AVOID,
    InformationOverloadTolerance.LOW,
    InformationOverloadTolerance.MEDIUM,
    InformationOverloadTolerance.HIGH,
)


VACANCY_INTERRUPTION_AXIS: Final = (
    InterruptionsTolerance.AVOID,
    InterruptionsTolerance.LOW,
    InterruptionsTolerance.MEDIUM,
    InterruptionsTolerance.HIGH,
)


VACANCY_NOISE_AXIS: Final = (
    NoiseTolerance.VERY_LOW,
    NoiseTolerance.LOW,
    NoiseTolerance.MEDIUM,
    NoiseTolerance.HIGH,
)


VACANCY_OPEN_SPACE_AXIS: Final = (
    OpenSpaceTolerance.VERY_LOW,
    OpenSpaceTolerance.LOW,
    OpenSpaceTolerance.MEDIUM,
    OpenSpaceTolerance.HIGH,
)


VACANCY_PHYSICAL_ACTIVITY_AXIS: Final = (
    PhysicalActivityTolerance.NEVER,
    PhysicalActivityTolerance.LOW,
    PhysicalActivityTolerance.MEDIUM,
    PhysicalActivityTolerance.HIGH,
)


VACANCY_STANDING_WORK_AXIS: Final = (
    StandingWorkTolerance.LOW,
    StandingWorkTolerance.MEDIUM,
    StandingWorkTolerance.HIGH,
)


VACANCY_TRAVEL_AXIS: Final = (
    TravelTolerance.NEVER,
    TravelTolerance.LOW,
    TravelTolerance.MEDIUM,
    TravelTolerance.HIGH,
)


VACANCY_TASK_STRUCTURE_AXIS: Final = (
    PreferredTaskStructure.HIGHLY_STRUCTURED,
    PreferredTaskStructure.STRUCTURED,
    PreferredTaskStructure.BALANCED,
    PreferredTaskStructure.FLEXIBLE,
    PreferredTaskStructure.OPEN_ENDED,
)


VACANCY_TASK_VARIETY_AXIS: Final = (
    TaskVarietyPreference.REPETITIVE,
    TaskVarietyPreference.MOSTLY_REPETITIVE,
    TaskVarietyPreference.BALANCED,
    TaskVarietyPreference.MOSTLY_DIVERSE,
    TaskVarietyPreference.HIGHLY_DIVERSE,
)


VACANCY_AUTONOMY_AXIS: Final = (
    AutonomyLevel.LOW,
    AutonomyLevel.MEDIUM,
    AutonomyLevel.HIGH,
)


VACANCY_FEEDBACK_FREQUENCY_AXIS: Final = (
    FeedbackFrequencyPreference.AS_NEEDED,
    FeedbackFrequencyPreference.OCCASIONAL,
    FeedbackFrequencyPreference.REGULAR,
    FeedbackFrequencyPreference.FREQUENT,
)


VACANCY_TEAM_SIZE_AXIS: Final = (
    PreferredTeamSize.SOLO,
    PreferredTeamSize.SMALL,
    PreferredTeamSize.MEDIUM,
    PreferredTeamSize.LARGE,
)


VACANCY_MANAGEMENT_STYLE_AXIS: Final = (
    PreferredManagementStyle.STRUCTURED,
    PreferredManagementStyle.SUPPORTIVE,
    PreferredManagementStyle.AUTONOMOUS,
    PreferredManagementStyle.COLLABORATIVE,
    PreferredManagementStyle.DIRECT,
    PreferredManagementStyle.FLEXIBLE,
)


VACANCY_WORK_FORMAT_AXIS: Final = (
    WorkFormat.REMOTE,
    WorkFormat.HYBRID,
    WorkFormat.OFFICE,
)


VACANCY_WEEKEND_WORK_AXIS: Final = (
    WeekendWork.USUALLY_WEEKENDS,
    WeekendWork.FLEXIBLE_DAYS_OFF,
    WeekendWork.WEEKENDS_ON_WEEKDAYS,
)


VACANCY_EDUCATION_AXIS: Final = (
    EducationLevel.SECONDARY_EDUCATION,
    EducationLevel.SPECIAL_EDUCATION,
    EducationLevel.INCOMPLETE_HIGHER_EDUCATION,
    EducationLevel.STUDENT_SPECIAL_EDUCATION,
    EducationLevel.STUDENT_HIGHTER_EDUCATION,
    EducationLevel.HIGHTER_EDUCATION,
)


VACANCY_AXES: Final = {
    'overtime': VACANCY_OVERTIME_AXIS,
    'night_work': VACANCY_NIGHT_WORK_AXIS,
    'shift_work': VACANCY_SHIFT_WORK_AXIS,
    'business_trip': VACANCY_BUSINESS_TRIP_AXIS,
    'client_communication': VACANCY_CLIENT_COMMUNICATION_AXIS,
    'team_communication': VACANCY_TEAM_COMMUNICATION_AXIS,
    'meetings': VACANCY_MEETING_AXIS,
    'public_speaking': VACANCY_PUBLIC_SPEAKING_AXIS,
    'phone_calls': VACANCY_PHONE_CALL_AXIS,
    'customer_support': VACANCY_CUSTOMER_SUPPORT_AXIS,
    'conflict': VACANCY_CONFLICT_AXIS,
    'multitasking': VACANCY_MULTITASKING_AXIS,
    'deadline': VACANCY_DEADLINE_AXIS,
    'context_switching': VACANCY_CONTEXT_SWITCHING_AXIS,
    'ambiguity': VACANCY_AMBIGUITY_AXIS,
    'information_overload': VACANCY_INFORMATION_OVERLOAD_AXIS,
    'interruptions': VACANCY_INTERRUPTION_AXIS,
    'noise': VACANCY_NOISE_AXIS,
    'open_space': VACANCY_OPEN_SPACE_AXIS,
    'physical_activity': VACANCY_PHYSICAL_ACTIVITY_AXIS,
    'standing_work': VACANCY_STANDING_WORK_AXIS,
    'travel': VACANCY_TRAVEL_AXIS,
    'task_structure': VACANCY_TASK_STRUCTURE_AXIS,
    'task_variety': VACANCY_TASK_VARIETY_AXIS,
    'autonomy': VACANCY_AUTONOMY_AXIS,
    'feedback_frequency': VACANCY_FEEDBACK_FREQUENCY_AXIS,
    'team_size': VACANCY_TEAM_SIZE_AXIS,
    'management_style': VACANCY_MANAGEMENT_STYLE_AXIS,
    'work_format': VACANCY_WORK_FORMAT_AXIS,
    'weekend_work': VACANCY_WEEKEND_WORK_AXIS,
    'education': VACANCY_EDUCATION_AXIS,
}
