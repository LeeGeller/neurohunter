"""Vacancy repository."""

from app.models.vacancy import Vacancy
from pymongo.asynchronous.database import AsyncDatabase


class VacancyRepository:
    """Vacancy repository."""

    def __init__(self, db: AsyncDatabase):
        self.collection = db["vacancies"]

    async def get_all_vacancies(self) -> list[Vacancy]:
        """Get all vacancies from the database."""
        vacancies = []

        cursor = self.collection.find({})

        async for vacancy in cursor:
            vacancy.pop("_id", None)
            vacancies.append(Vacancy(**vacancy))

        return vacancies
