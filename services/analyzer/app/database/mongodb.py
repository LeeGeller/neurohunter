"""MongoDB connection."""

from pymongo import (
    AsyncMongoClient,
)

from app.config.settings import (
    MONGO_URI,
)


def create_mongo_client() -> AsyncMongoClient:
    """Create a MongoDB client."""
    return AsyncMongoClient(MONGO_URI)
