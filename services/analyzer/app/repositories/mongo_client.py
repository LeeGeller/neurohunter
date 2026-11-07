from pymongo import (
    AsyncMongoClient,
)

from app.config import (
    settings,
)

mongo_client = AsyncMongoClient(settings.mongo_uri)
mongo_db = mongo_client[settings.mongo_db]
