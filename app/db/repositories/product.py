from typing import List, Optional
from app.db.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    async def find_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[dict]:
        return await self.find_all({"category": category}, skip=skip, limit=limit)

    async def find_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> List[dict]:
        query = {
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        }
        return await self.find_all(query, skip=skip, limit=limit)

    async def update_stock(self, id: str, quantity: int) -> Optional[dict]:
        query = {"_id": id}
        update = {"$inc": {"stock": -quantity}}
        return await self.collection.find_one_and_update(query, update, return_document=True) 