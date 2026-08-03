"""Vacancy repository."""

from typing import (
    Optional,
    Union,
)

from pymongo.asynchronous.database import AsyncDatabase

class VacancyRepository:
    """Vacancy repository."""

    def __init__(self, db: AsyncDatabase):
        self.collection = db["vacancies"]

    async def get_all_vacancies(self) -> list[dict[str, Optional[Union[str, int]]]]:
        """Get all vacancies from the database."""
        vacancies = []

        cursor = self.collection.find({})

        async for vacancy in cursor:
            vacancy["_id"] = str(vacancy["_id"])
            vacancies.append(vacancy)

        return vacancies
