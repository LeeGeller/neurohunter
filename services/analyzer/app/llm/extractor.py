import json
from typing import (
    Optional,
)
from typing import (
    Optional,
)

from app.llm.client import (
    OllamaClient,
)
from app.llm.prompts import (
    RESUME_FEATURES_PROMPT,
    USER_FEATURES_PROMPT,
    VACANCY_FEATURES_PROMPT,
    VACANCY_REQUIREMENTS_PROMPT,
)
from app.models.user import (
    UserProfile,
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
from app.schemas.user.resume_features import (
    ResumeFeaturesSchema,
)
from app.schemas.vacancy.vacancy_features import (
    VacancyFeaturesSchema,
)
from app.schemas.vacancy.vacancy_requirements import (
    VacancyRequirementsSchema,
)


class VacancyFeaturesExtractor:
    """Analyze vacancies using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_schema: Optional[dict] = None,
    ) -> None:
        """Initialize the VacancyFeaturesExtractor."""
        self.llm_client = llm_client
        self.response_schema = response_schema


    async def extract_features(self, vacancy: Vacancy) -> VacancyFeaturesSchema:
        """Extract structured features from a vacancy using LLM."""

        prompt = VACANCY_FEATURES_PROMPT.format(
            title=vacancy.title,
            company=vacancy.company,
            work_location=vacancy.work_location or "",
            work_format=vacancy.work_format or "",
            salary_from=vacancy.salary_from or "",
            salary_to=vacancy.salary_to or "",
            description=vacancy.description,

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
        )

        response = await self.llm_client.generate(
            prompt,
            self.response_schema,
        )

        features = VacancyFeaturesSchema.model_validate_json(response)

        return features


class ResumeFeaturesExtractor:
    """Analyze resumes using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_schema: Optional[dict] = None,
    ) -> None:
        """Initialize the ResumeFeaturesExtractor."""
        self.llm_client = llm_client
        self.response_schema = response_schema

    async def extract_features(self, resume: str) -> ResumeFeaturesSchema:
        """Extract structured features from a resume using LLM."""

        prompt = RESUME_FEATURES_PROMPT.format(
            resume_text=resume
        )

        response = await self.llm_client.generate(
            prompt,
            self.response_schema,
        )

        resume_features = ResumeFeaturesSchema.model_validate_json(response)

        return resume_features


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


class VacancyRequirementsExtractor:
    """Analyze vacancy requirements using LLM."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_schema: Optional[dict],
    ) -> None:
        """Initialize the VacancyRequirementsExtractor."""
        self.llm_client = llm_client
        self.response_schema = response_schema

    async def extract_requirements(self, vacancy: Vacancy) -> VacancyRequirementsSchema:
        """Extract structured requirements from a vacancy using LLM."""

        prompt = VACANCY_REQUIREMENTS_PROMPT.format(
            title=vacancy.title,
            description=vacancy.description,
        )

        response = await self.llm_client.generate(
            prompt,
            self.response_schema,
        )

        requirement = VacancyRequirementsSchema.model_validate_json(response)

        return requirement
