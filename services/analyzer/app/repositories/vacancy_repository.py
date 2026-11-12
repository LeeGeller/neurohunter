"""Vacancy repository."""

from pymongo.asynchronous.database import (
    AsyncDatabase,
)

from app.models.vacancy import (
    Vacancy,
)


class VacancyRepository:
    """Vacancy repository."""

    def __init__(self, db: AsyncDatabase):
        self.collection = db['vacancies']

    async def get_vacancies_to_analyze(self) -> list[Vacancy]:
        """Get all vacancies from the database."""
        vacancies = []

        cursor = self.collection.find({})

        async for vacancy in cursor:
            vacancy.pop('_id', None)
            vacancies.append(Vacancy(**vacancy))

        return vacancies

    async def get_vacancies_by_ids(
        self,
        vacancy_ids: list[str],
    ) -> list[Vacancy]:
        """Get vacancies by IDs."""

        vacancies = []

        cursor = self.collection.find({
            'vacancy_id': {
                '$in': vacancy_ids,
            },
        })

        async for vacancy in cursor:
            vacancy.pop('_id', None)
            vacancies.append(Vacancy(**vacancy))

        return vacancies
