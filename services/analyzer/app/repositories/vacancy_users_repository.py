"""VacancyUsers Repository."""

from pymongo.asynchronous.database import (
    AsyncDatabase,
)

from app.models.vacancy_users import (
    VacancyUsers,
)


class VacancyUsersRepository:
    """VacancyUsers repository."""

    def __init__(self, db: AsyncDatabase):
        self.collection = db['vacancy_users']

    async def get_all_vacancy_users(self) -> list[VacancyUsers]:
        """Get all vacancy users from the database."""
        vacancy_users = []

        cursor = self.collection.find({})

        async for vacancy_user in cursor:
            vacancy_user.pop("_id", None)
            vacancy_users.append(VacancyUsers(**vacancy_user))

        return vacancy_users


    async def get_vacancy_users_by_vacancy_id(self, vacancy_id: str) -> list[VacancyUsers]:
        """Get vacancy users by vacancy ID from the database."""
        vacancy_users = []

        cursor = self.collection.find({"vacancy_id": vacancy_id})

        async for vacancy_user in cursor:
            vacancy_user.pop("_id", None)
            vacancy_users.append(VacancyUsers(**vacancy_user))

        return vacancy_users

    async def get_vacancy_users_by_user_id(self, user_id: str) -> list[VacancyUsers]:
        """Get vacancy users by user ID from the database."""
        vacancy_users = []

        cursor = self.collection.find({"user_id": user_id})

        async for vacancy_user in cursor:
            vacancy_user.pop("_id", None)
            vacancy_users.append(VacancyUsers(**vacancy_user))

        return vacancy_users
