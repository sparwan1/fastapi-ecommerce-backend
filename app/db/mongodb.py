from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client = None  # type: AsyncIOMotorClient
    db = None

    async def connect_to_database(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]

    async def close_database_connection(self):
        self.client.close()

mongodb = MongoDB() 