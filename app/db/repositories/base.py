from typing import Any, List, Optional, TypeVar
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.base import BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)  # Not used, can be removed

class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_one(self, query: dict) -> Optional[dict]:
        return await self.collection.find_one(query)

    async def find_all(self, query: dict = None, skip: int = 0, limit: int = 100) -> List[dict]:
        cursor = self.collection.find(query or {}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def create(self, data: dict) -> dict:
        result = await self.collection.insert_one(data)
        return await self.find_one({"_id": result.inserted_id})

    async def update(self, id: str, data: dict) -> Optional[dict]:
        query = {"_id": ObjectId(id)}
        update = {"$set": data}
        await self.collection.update_one(query, update)
        return await self.find_one(query)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0 