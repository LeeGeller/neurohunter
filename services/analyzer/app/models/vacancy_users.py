"""VacancyUsers Model."""

from pydantic import (
    BaseModel,
)


class VacancyUsers(BaseModel):
    """VacancyUsers model."""

    vacancy_id: str
    user_id: str
