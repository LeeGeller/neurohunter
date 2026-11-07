"""MongoDB client."""


from pymongo import (
    AsyncMongoClient,
)
from pymongo.asynchronus.database import (
    AsyncDatabase,
)

from app.config import (
    settings,
)


class MongoDBClient:
    """MongoDB connection client."""

    def __init__(self):
        self.client : AsyncMongoClient | None = None
        self.db : AsyncDatabase | None = None

    async def connect(self) -> None:
        """Connect to the MongoDB database."""
        self.client = AsyncMongoClient(settings.mongo_uri)
        self.db = self.client[settings.mongo_db]

        await self.client.admin.command("ping")

    async def disconnect(self) -> None:
        """Disconnect from the MongoDB database."""
        if self.client:
            await self.client.close()
            self.client = None
            self.db = None

    def get_database(self) -> AsyncDatabase:
        """Get the MongoDB database instance."""
        if not self.db:
            raise RuntimeError("MongoDB client is not connected.")
        return self.db
