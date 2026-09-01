"""User profile schemas."""

import uuid

from pydantic import (
    BaseModel,
)


class UserProfileSchema(BaseModel):
    """User profile schema.

    Info about the user, including personal details, preferences, and tolerances.
    User fills this form after registration.
    """

    user_id: uuid.UUID

    age: int
    profession: str | None = None
    experience_years: float | None = None
    education: str | None = None

    # Work preferences and tolerances
    preferred_work_days_per_week: float | None = None
    preferred_work_hours_per_day: float | None = None
    flexible_schedule_needed: bool | None = None
    overtime_tolerance: str | None = None
    preferred_end_time: str | None = None
    weekend_work_tolerance: str | None = None
    night_work_tolerance: str | None = None
    shift_work_tolerance: str | None = None
    business_trip_tolerance: str | None = None

    # Communication preferences and tolerances
    client_communication_tolerance: str | None = None
    team_communication_tolerance: str | None = None
    meeting_tolerance: str | None = None
    public_speaking_tolerance: str | None = None
    phone_call_tolerance: str | None = None
    customer_support_tolerance: str | None = None
    conflict_tolerance: str | None = None

    # Task management preferences and tolerances
    multitasking_tolerance: str | None = None
    deadline_tolerance: str | None = None
    context_switching_tolerance: str | None = None
    ambiguity_tolerance: str | None = None
    information_overload_tolerance: str | None = None
    interruptions_tolerance: str | None = None

    # Stress management preferences and tolerances
    burnout_sensitivity: str | None = None
    social_overload_sensitivity: str | None = None
    preferred_team_size: str | None = None
    preferred_management_style: str | None = None
    preferred_task_structure: str | None = None
    autonomy_level: str | None = None
    instruction_detail_preference: str | None = None
    feedback_frequency_preference: str | None = None

    # Work environment preferences and tolerances
    noise_tolerance: str | None = None
    open_space_tolerance: str | None = None
    office_presence_tolerance: str | None = None
    home_work_environment: str | None = None

    # Work preferences
    preferred_work_formats: list[str]

    # Work tolerancesW
    physical_activity_tolerance: str | None = None
    standing_work_tolerance: str | None = None
    travel_tolerance: str | None = None

    # Work factors
    motivation_factors: list[str]
    career_growth_importance: float | None = None
    stability_importance: float | None = None
    income_importance: float | None = None
    interesting_tasks_importance: float | None = None
    social_environment_importance: float | None = None
    work_life_balance_importance: float | None = None

    # Work conditions
    conditions: list[str]

    # Other information. For example, a short description of the user.
    about_me: str | None = None
