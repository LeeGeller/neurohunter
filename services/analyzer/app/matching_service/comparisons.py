
from datetime import (
    time,
)


def compare_preferred_salary(
    user_value: float,
    vacancy_value: float,
    max_difference: float,
) -> float:
    """Compare preferred salary with vacancy salary.

    Return 1.0 if the vacancy minimum salary meets or exceeds the user's
    preference. Otherwise, linearly decrease the compatibility score
    as the salary difference increases, reaching 0.0 at max_difference.
    """

    difference = user_value - vacancy_value

    return (
        1.0
        if difference <=0
        else
        max(0.0, 1.0 - difference/max_difference)

    )

def compare_preferred_numeric_values(
    user_value: float,
    vacancy_value: float,
    max_difference: float,
) -> float:
    """Compare numerical values based on the user's preferred direction.

    Return 1.0 if the vacancy value meets or exceeds the user's preference
    in the favorable direction. Otherwise, linearly decrease the compatibility
    score as the difference increases, reaching 0.0 at max_difference.
    Use to with work_days_per_week and work_hours_per_day.

    Lower vacancy values are considered favorable.
    """
    difference = vacancy_value - user_value

    return (
        1.0
        if difference <= 0
        else
        max(0.0, 1.0 - difference/max_difference)
    )


def compare_preferred_time(
    user_value: time,
    vacancy_value: time,
    max_difference: float,
) -> float:
    """Compare preferred time with vacancy time.

    Return 1.0 for an exact match. Linearly decrease the compatibility
    score as the time difference increases, reaching 0.0 at max_difference.
    """

    user_minutes = user_value.hour * 60 + user_value.minute
    vacancy_minutes = vacancy_value.hour * 60 + vacancy_value.minute

    difference = abs(user_minutes - vacancy_minutes)

    return max(0.0, 1.0 - difference/max_difference)
