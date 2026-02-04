from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI, MONGO_DB_NAME
from ..logging import LOGGER
LOGGER(__name__).info('Connecting to your Mongo Database...')
try:
    # Fail fast if server selection fails (timeout in ms)
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000)
    # Use configured database name instead of a hardcoded attribute
    mongodb = _mongo_async_[MONGO_DB_NAME]
    LOGGER(__name__).info('MongoDB client created (server connection will be attempted lazily).')
except Exception as e:
    LOGGER(__name__).error(f'Failed to initialize MongoDB client: {e}')
    exit(1)
