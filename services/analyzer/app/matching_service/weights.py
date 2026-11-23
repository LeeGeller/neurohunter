from typing import (
    Optional,
)

from app.matching_service.user_axes import (
    NumericalWeights,
)
from app.models.user import (
    UserProfile,
)


def get_numerical_weights(
    profile: UserProfile
) -> NumericalWeights:
    """Get normalized importance weights from user profile."""
    return {
        'salary': normilize_importance(profile.income_importance),
        'work_days_per_week': normilize_importance(
            profile.work_life_balance_importance,
        ),
        'work_hours_per_day': normilize_importance(
            profile.work_life_balance_importance
        ),
        'start_time': normilize_importance(
            profile.flexible_schedule_needed_importance,
        ),
        'end_time': normilize_importance(
            profile.flexible_schedule_needed_importance,
        ),
    }


def normilize_importance(
    importance: Optional[int]
) -> float:
    """Normalize importance value to [0, 1]."""
    return (
        importance / 5
        if importance
        else 1.0
    )
