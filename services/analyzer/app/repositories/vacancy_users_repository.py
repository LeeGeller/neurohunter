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
        self.collection = db["vacancy_users"]

    async def get_all_vacancy_users(self) -> list[VacancyUsers]:
        """Get all vacancy users from the database."""
        vacancy_users = []

        cursor = self.collection.find({})

        async for vacancy_user in cursor:
            vacancy_user.pop("_id", None)
            vacancy_users.append(VacancyUsers(**vacancy_user))

        return vacancy_users
