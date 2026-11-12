"""Vacancy Context Service module."""
from app.models.vacancy import (
    Vacancy,
)
from app.models.vacancy_users import (
    VacancyUsers,
)
from app.repositories.vacancy_repository import (
    VacancyRepository,
)
from app.repositories.vacancy_users_repository import (
    VacancyUsersRepository,
)


class VacancyContextService:
    """Facade for accessing vacancies and vacancy-user relationships."""

    def __init__(self,
        vacancy_repository: VacancyRepository,
        vacancy_users_repository: VacancyUsersRepository,
    ):
        self.vacancy = vacancy_repository
        self.vacancy_users = vacancy_users_repository

    async def get_vacancies_to_analyze(self) -> list[Vacancy]:
        """Get all vacancies available for analysis."""

        return await self.vacancy.get_vacancies_to_analyze()

    async def get_vacancies_by_ids(
        self,
        vacancy_ids: list[str],
    ) -> list[Vacancy]:
        """Get vacancies by their IDs."""

        return await self.vacancy.get_vacancies_by_ids(vacancy_ids)

    async def get_all_vacancy_users(self) -> list[VacancyUsers]:
        """Get all vacancy-user relationships."""

        return await self.vacancy_users.get_all_vacancy_users()

    async def get_vacancy_users_by_vacancy_id(
        self,
        vacancy_id: str,
    ) -> list[VacancyUsers]:
        """Get users associated with a vacancy."""

        return await self.vacancy_users.get_vacancy_users_by_vacancy_id(
            vacancy_id,
        )

    async def get_vacancy_users_by_user_id(
        self,
        user_id: str,
    ) -> list[VacancyUsers]:
        """Get vacancies associated with a user."""

        return await self.vacancy_users.get_vacancy_users_by_user_id(
            user_id,
        )

    async def get_vacancies_by_user_id(
        self,
        user_id: str,
    ) -> list[Vacancy]:
        """Get vacancies associated with a user."""

        vacancy_users = await self.get_vacancy_users_by_user_id(user_id)

        vacancy_ids = [
            vacancy_user.vacancy_id
            for vacancy_user in vacancy_users
        ]

        return await self.get_vacancies_by_ids(vacancy_ids)
