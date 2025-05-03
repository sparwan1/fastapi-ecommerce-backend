from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

class CartItemInDB(BaseModel):
    id: str
    product_id: str
    quantity: int
    price: float

    class Config:
        from_attributes = True

class CartBase(BaseModel):
    user_id: str
    items: List[CartItemInDB] = []
    total: Decimal = Decimal('0.00')

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    is_active: Optional[bool] = None

class CartInDB(CartBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True

def cart_helper(cart: dict) -> dict:
    return {
        "id": str(cart["_id"]),
        "user_id": cart["user_id"],
        "items": [
            {
                "id": item.get("id", ""),
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": float(item["price"])
            }
            for item in cart.get("items", [])
        ],
        "total": float(cart.get("total", 0)),
        "is_active": cart.get("is_active", True),
    } 