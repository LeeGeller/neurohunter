"""User features schemas."""

from pydantic import (
    BaseModel,
)


class UserFeatures(BaseModel):
    """User features model for LLM."""

    user_id: str

    preferred_work_days_per_week: float | None
    preferred_work_hours_per_day: float | None
    preferred_weekly_hours: float | None

    flexible_schedule_needed: bool | None
    overtime_tolerance: str | None

    client_communication_tolerance: str | None
    team_communication_tolerance: str | None
    meeting_tolerance: str | None
    communication_frequency_preference: str | None

    multitasking_tolerance: str | None
    task_predictability_preference: str | None
    task_clarity_requirement: str | None
    task_independence_preference: str | None

    deadline_tolerance: str | None
    burnout_sensitivity: str | None
    social_overload_sensitivity: str | None

    preferred_team_size: str | None
    preferred_management_style: str | None

    evidence: list[str]
