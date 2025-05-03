from typing import List, Optional
from bson import ObjectId
from app.db.repositories.base import BaseRepository
from app.models.cart import Cart

class CartRepository(BaseRepository):
    async def find_by_user_id(self, user_id: str) -> Optional[dict]:
        return await self.find_one({"user_id": str(user_id)})

    async def add_item(self, cart_id: str, item: dict) -> dict:
        cart = await self.find_one({"_id": ObjectId(cart_id)})
        if not cart:
            return None

        items = cart.get("items", [])
        found = False
        for cart_item in items:
            if cart_item["product_id"] == item["product_id"]:
                cart_item["quantity"] += item["quantity"]
                found = True
                break

        if not found:
            items.append(item)

        # Recalculate total
        total = sum(i["quantity"] * i["price"] for i in items)

        update = {
            "$set": {
                "items": items,
                "total": total
            }
        }
        await self.collection.update_one({"_id": ObjectId(cart_id)}, update)
        return await self.find_one({"_id": ObjectId(cart_id)})

    async def remove_item(self, cart_id: str, item_id: str) -> Optional[dict]:
        query = {"_id": ObjectId(cart_id)}
        cart = await self.find_one(query)
        if not cart:
            return None

        # Find the item and its price * quantity to subtract from total
        item = next((item for item in cart["items"] if str(item["id"]) == item_id), None)
        if not item:
            return None

        update = {
            "$pull": {"items": {"id": item_id}},
            "$inc": {"total": -(float(item["price"]) * item["quantity"])}
        }
        return await self.collection.find_one_and_update(query, update, return_document=True)

    async def clear_cart(self, cart_id: str) -> Optional[dict]:
        query = {"_id": ObjectId(cart_id)}
        update = {
            "$set": {
                "items": [],
                "total": 0
            }
        }
        return await self.collection.find_one_and_update(query, update, return_document=True) 