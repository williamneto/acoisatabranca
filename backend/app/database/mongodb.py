from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from app.core.config import settings

# logger.debug("Connecting to mongodb...")

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def get_db_client() -> AsyncIOMotorClient:
    return db.client[settings.MONGO_DB_NAME]


async def connect_db():
    """Create database connection."""
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    logger.debug(f"Connecting to MongoDB {settings.MONGO_URI}")


async def close_db():
    """Close database connection."""
    db.client.close()
    logger.debug("Disconnecting from mongodb")

