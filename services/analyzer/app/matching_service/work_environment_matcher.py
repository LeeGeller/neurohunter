import uuid
from datetime import (
    time,
)
from typing import (
    Optional,
    TypedDict,
)

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.matching_service.comparisons import (
    compare_preferred_numeric_values,
    compare_preferred_salary,
    compare_preferred_time,
)
from app.matching_service.user_axes import (
    NumericalWeights,
)
from app.matching_service.weights import (
    get_numerical_weights,
)
from app.models.user import (
    UserProfile,
)
from app.models.vacancy import (
    VacancyFeatures,
)


class UserProfileNumericalValues(TypedDict):
    """Numerical values for matrix."""

    salary: Optional[int]
    work_days_per_week: Optional[float]
    work_hours_per_day: Optional[float]
    start_time: Optional[time]
    end_time: Optional[time]


class VacancyFeaturesNumericalValues(TypedDict):
    """Numerical values for matrix."""

    salary_min: Optional[float]
    salary_max: Optional[float]
    work_days_per_week: Optional[float]
    work_hours_per_day: Optional[float]
    start_time: Optional[time]
    end_time: Optional[time]


class WorkEnvironmentMatcher:
    """Match user work environment preferences against vacancy conditions."""

    def __init__(self, session: AsyncSession):
        """Initialize."""

        self.session = session

    async def get_vacancy_features(
        self,
        vacancy_id: uuid.UUID,
    ) -> Optional[VacancyFeatures]:
        """Get VacancyFeatures by id."""

        result = await self.session.execute(
            select(VacancyFeatures).where(
                VacancyFeatures.vacancy_id == vacancy_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_user_profile(
        self,
        user_id: uuid.UUID,
    ) -> Optional[UserProfile]:
        """Get UserProfile by id."""

        result = self.session.execute(
            select(UserProfile).where(
                UserProfile.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    def get_user_numerical_values(
        self,
        profile: UserProfile,
    ) -> UserProfileNumericalValues:
        """Get numerical values from user profile."""
        return {
            'salary': profile.salary,
            'work_days_per_week': profile.preferred_work_days_per_week,
            'work_hours_per_day': profile.preferred_work_hours_per_day,
            'start_time': profile.preferred_start_time,
            'end_time': profile.preferred_end_time,
        }

    def get_vacancy_numerical_values(
        self,
        vacancy_features: VacancyFeatures,
    ) -> VacancyFeaturesNumericalValues:
        """Get numerical values from vacancy features."""
        return {
            'salary_min': vacancy_features.salary_min,
            'salary_max': vacancy_features.salary_max,
            'work_days_per_week': vacancy_features.work_days_per_week,
            'work_hours_per_day': vacancy_features.work_hours_per_day,
            'start_time': vacancy_features.start_time,
            'end_time': vacancy_features.end_time,
        }

    def get_user_numerical_weights(
        self,
        profile: UserProfile,
    ) -> NumericalWeights:
        """Get numerical weifhts for user numerical values."""
        return get_numerical_weights(profile=profile)

    def calculate_numerical_compatibility(
        self,
        profile: UserProfile,
        vacancy_values: VacancyFeaturesNumericalValues,
        max_difference_salary: float,
        max_difference_work_days: float,
        max_difference_preferred_time: float,
    ):
        """Calculate weighted compatibility scores for numerical work conditions.

        Compare the user's preferences with vacancy values and account for
        the importance of each parameter. Return individual scores by parameter.
        """

        weights = self.get_user_numerical_weights(profile)

        results = {}

        vacancy_salary_min = vacancy_values.get('salary_min')
        vacancy_work_days = vacancy_values.get('work_days_per_week')
        vacancy_start_time = vacancy_values.get('start_time')

        if profile.salary and vacancy_salary_min:
            score = compare_preferred_salary(
                profile.salary,
                vacancy_salary_min,
                max_difference_salary,
            )
            results['salary'] = score * weights['salary']

        if (
            profile.preferred_work_days_per_week
            and vacancy_work_days
        ):
            score = compare_preferred_numeric_values(
                profile.preferred_work_days_per_week,
                vacancy_work_days,
                max_difference_work_days,
            )
            results['work_days_per_week'] = (
                score * weights['work_days_per_week']
            )

        if (
            profile.preferred_start_time
            and vacancy_start_time
        ):
            score = compare_preferred_time(
                profile.preferred_start_time,
                vacancy_start_time,
                max_difference_preferred_time,
            )
            results['start_time'] = score * weights['start_time']

        return results
