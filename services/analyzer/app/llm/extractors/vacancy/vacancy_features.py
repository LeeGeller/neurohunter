"""Vacancy features extractor."""

from app.llm.client import (
    OllamaClient,
)
from app.llm.extractors.base import (
    BaseExtractor,
)
from app.llm.prompts import (
    VACANCY_FEATURES_PROMPT,
)
from app.models.vacancy import (
    Vacancy,
)
from app.schemas.user.profile_enums import (
    AmbiguityTolerance,
    AutonomyLevel,
    BusinessTripTolerance,
    ContextSwitchingTolerance,
    DeadlineTolerance,
    FeedbackFrequencyPreference,
    MeetingTolerance,
    NightWorkTolerance,
    NoiseTolerance,
    PhoneCallTolerance,
    PhysicalActivityTolerance,
    PreferredTaskStructure,
    PublicSpeakingTolerance,
    ShiftWorkTolerance,
    TaskVarietyPreference,
    WeekendWork,
)
from app.schemas.vacancy.vacancy_features import (
    VacancyFeaturesSchema,
)


class VacancyFeaturesExtractor(
    BaseExtractor[VacancyFeaturesSchema]
):
    """Extract working conditions from vacancies."""

    def __init__(
        self,
        llm_client: OllamaClient,
    ) -> None:
        super().__init__(
            llm_client=llm_client,
            response_model=VacancyFeaturesSchema,
        )

    async def extract_features(
        self,
        vacancy: Vacancy,
    ) -> VacancyFeaturesSchema:
        """Extract structured features from a vacancy."""

        prompt = VACANCY_FEATURES_PROMPT.format(
            title=vacancy.title,
            company=vacancy.company,
            work_location=vacancy.work_location or '',
            work_format=vacancy.work_format or '',
            salary_from=vacancy.salary_from or '',
            salary_to=vacancy.salary_to or '',
            description=vacancy.description,

            night_work_values=', '.join(
                item.value for item in NightWorkTolerance
            ),
            shift_work_values=', '.join(
                item.value for item in ShiftWorkTolerance
            ),
            business_trip_values=', '.join(
                item.value for item in BusinessTripTolerance
            ),
            weekend_work_values=', '.join(
                item.value for item in WeekendWork
            ),
            meeting_values=', '.join(
                item.value for item in MeetingTolerance
            ),
            phone_call_values=', '.join(
                item.value for item in PhoneCallTolerance
            ),
            public_speaking_values=', '.join(
                item.value for item in PublicSpeakingTolerance
            ),
            deadline_values=', '.join(
                item.value for item in DeadlineTolerance
            ),
            context_switching_values=', '.join(
                item.value for item in ContextSwitchingTolerance
            ),
            task_structure_values=', '.join(
                item.value for item in PreferredTaskStructure
            ),
            task_variety_values=', '.join(
                item.value for item in TaskVarietyPreference
            ),
            autonomy_values=', '.join(
                item.value for item in AutonomyLevel
            ),
            feedback_values=', '.join(
                item.value for item in FeedbackFrequencyPreference
            ),
            noise_values=', '.join(
                item.value for item in NoiseTolerance
            ),
            physical_activity_values=', '.join(
                item.value for item in PhysicalActivityTolerance
            ),
            ambiguity_values=', '.join(
                item.value for item in AmbiguityTolerance
            ),
        )

        return await self.generate(prompt=prompt)
