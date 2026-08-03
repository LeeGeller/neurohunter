from datetime import datetime

from pydantic import BaseModel, Field


class Vacancy(BaseModel):
    """Vacancy model."""

    id: str
    title: str
    vacancy_date: datetime = Field(alias="vacancydate")
    description: str
    company: str
    work_location: str | None = Field(alias="worklocation")
    work_format: str | None = Field(alias="workformat")
    salary_from: int | None = Field(alias="salaryfrom")
    salary_to: int | None = Field(alias="salaryto")
    currency: str | None
    url: str


class VacancyAnalysis(BaseModel):
    """Analysis of the vacancy itself."""

    vacancy_id: str

    # Job difficulty
    difficulty: float

    # Estimated workload
    workload: float

    # Social load
    social_overload: float

    # Communication load
    communication_load: float

    # Uncertainty level
    uncertainty_level: float

    # Overtime risk
    overtime_risk: float

    # Positive aspects of the vacancy
    strengths: list[str]

    # Potential problems
    risks: list[str]

    # Questions worth clarifying
    questions_to_ask: list[str]


class VacancyMatch(BaseModel):
    """Personalized vacancy match for a user."""

    vacancy_id: str
    user_id: str

    # Overall profile match
    profile_match: float

    # Professional skills match
    skills_match: float

    # Experience match
    experience_match: float

    # Work format match
    work_format_match: float

    # Personal burnout risk
    burnout_risk: float

    # Personal workload risk
    workload_risk: float

    # Personal social overload risk
    social_overload_risk: float

    # Why the vacancy is a good/bad fit
    explanation: str
