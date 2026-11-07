"""Vacancy Context Service module."""
from app.models.vacancy import (
    Vacancy,
)
from app.models.vacancy_users import (
    VacancyUsers,
)
from app.repositories.repository_manager import (
    RepositoryManager,
)


class VacancyContextService:
    """Vacancy Context Service.

    This service provides methods to interact with the vacancy context.
    """

    def __init__(self, repositories: RepositoryManager):
        self.repositories = repositories

    async def get_all_vacancy_users(self) -> list[VacancyUsers]:
        """Get all vacancy users."""
        return await self.repositories.vacancy_users.get_all_vacancy_users()

    async def get_all_vacancies(self) -> list[Vacancy]:
        """Get all vacancies."""
        return await self.repositories.vacancy.get_all_vacancies()

    async def get_vacancy_users_by_vacancy_id(
        self,
        vacancy_id: str
    ) -> list[VacancyUsers]:
        """Get vacancy users by vacancy ID."""
        return await self.repositories.vacancy_users.get_vacancy_users_by_vacancy_id(vacancy_id)

    async def get_vacancy_users_by_user_id(
        self,
        user_id: str
    ) -> list[VacancyUsers]:
        """Get vacancy users by user ID."""
        return await self.repositories.vacancy_users.get_vacancy_users_by_user_id(user_id)
