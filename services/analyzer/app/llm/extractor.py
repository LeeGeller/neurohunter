import json

from app.llm.client import (
    OllamaClient,
)
from app.llm.prompts import (
    RESUME_FEATURES_PROMPT,
    USER_FEATURES_PROMPT,
    VACANCY_FEATURES_PROMPT,
)
from app.models.user import (
    UserProfile,
)
from app.models.vacancy import (
    Vacancy,
    VacancyFeatures,
)
from app.schemas.profile_enums import (
    AmbiguityTolerance,
    AutonomyLevel,
    BusinessTripTolerance,
    ContextSwitchingTolerance,
    DeadlineTolerance,
    FeedbackFrequencyPreference,
    InformationOverloadTolerance,
    InterruptionsTolerance,
    MeetingTolerance,
    NightWorkTolerance,
    NoiseTolerance,
    OvertimeTolerance,
    PhoneCallTolerance,
    PhysicalActivityTolerance,
    PreferredTaskStructure,
    PublicSpeakingTolerance,
    ShiftWorkTolerance,
    TaskVarietyPreference,
    WeekendWork,
)


class VacancyFeaturesExtractor:
    """Analyze vacancies using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_features(self, vacancy: Vacancy) -> VacancyFeatures:
        """Extract structured features from a vacancy using LLM."""

        prompt = VACANCY_FEATURES_PROMPT.format(
            vacancy_id=vacancy.id,
            title=vacancy.title,
            company=vacancy.company,
            work_location=vacancy.work_location or "",
            work_format=vacancy.work_format or "",
            salary_from=vacancy.salary_from or "",
            salary_to=vacancy.salary_to or "",
            description=vacancy.description,

            overtime_values=", ".join(
                item.value for item in OvertimeTolerance
            ),
            night_work_values=", ".join(
                item.value for item in NightWorkTolerance
            ),
            shift_work_values=", ".join(
                item.value for item in ShiftWorkTolerance
            ),
            business_trip_values=", ".join(
                item.value for item in BusinessTripTolerance
            ),
            weekend_work_values=", ".join(
                item.value for item in WeekendWork
            ),
            meeting_values=", ".join(
                item.value for item in MeetingTolerance
            ),
            phone_call_values=", ".join(
                item.value for item in PhoneCallTolerance
            ),
            public_speaking_values=", ".join(
                item.value for item in PublicSpeakingTolerance
            ),
            deadline_values=", ".join(
                item.value for item in DeadlineTolerance
            ),
            context_switching_values=", ".join(
                item.value for item in ContextSwitchingTolerance
            ),
            task_structure_values=", ".join(
                item.value for item in PreferredTaskStructure
            ),
            task_variety_values=", ".join(
                item.value for item in TaskVarietyPreference
            ),
            autonomy_values=", ".join(
                item.value for item in AutonomyLevel
            ),
            feedback_values=", ".join(
                item.value for item in FeedbackFrequencyPreference
            ),
            noise_values=", ".join(
                item.value for item in NoiseTolerance
            ),
            physical_activity_values=", ".join(
                item.value for item in PhysicalActivityTolerance
            ),
            ambiguity_values=", ".join(
                item.value for item in AmbiguityTolerance
            ),
            information_load_values=", ".join(
                item.value for item in InformationOverloadTolerance
            ),
            interruptions_values=", ".join(
                item.value for item in InterruptionsTolerance
            ),
        )

        response = await self.llm_client.generate(prompt)

        return VacancyFeatures.model_validate_json(response)


class ResumeFeaturesExtractor:
    """Analyze resumes using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_features(self, resume: str) -> dict:
        """Extract structured features from a resume using LLM."""

        prompt = RESUME_FEATURES_PROMPT.format(
            resume_text=resume
        )

        response = await self.llm_client.generate(prompt)

        return json.loads(response)


class UserFeaturesExtractor:
    """Analyze users using LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client

    async def extract_features(self, user: UserProfile) -> dict:
        """Extract structured features from a user using LLM."""

        profile_dict = self.profile_to_dict(user)
        prompt = USER_FEATURES_PROMPT.format(**profile_dict)

        response = await self.llm_client.generate(prompt)

        return json.loads(response)

    def profile_to_dict(self, user: UserProfile) -> dict:
        """Convert UserProfile object to dictionary."""
        return {
            column.name: getattr(user, column.name)
            for column in user.__table__.columns
        }
