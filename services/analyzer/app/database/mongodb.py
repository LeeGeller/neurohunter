"""MongoDB connection."""

from pymongo import (
    AsyncMongoClient,
)

from app.config.settings import (
    settings,
)


def create_mongo_client() -> AsyncMongoClient:
    """Create a MongoDB client."""
    return AsyncMongoClient(settings.mongo_uri)
