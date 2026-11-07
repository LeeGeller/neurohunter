"""Repository Manager."""

from app.database.mongo_client import (
    MongoDBClient,
)
from app.repositories.vacancy_repository import (
    VacancyRepository,
)
from app.repositories.vacancy_users_repository import (
    VacancyUsersRepository,
)


class RepositoryManager:
    """Repository Manager.

    This class manages the repositories for different models.
    """

    def __init__(self, mongo_client: MongoDBClient):
        db = mongo_client.get_database()

        self.vacancy = VacancyRepository(db)
        self.vacancy_users = VacancyUsersRepository(db)
