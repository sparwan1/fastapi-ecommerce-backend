from typing import List, Optional
from decimal import Decimal
from app.models.base import BaseDBModel

class CartItem(BaseDBModel):
    product_id: str
    quantity: int
    price: Decimal

class Cart(BaseDBModel):
    user_id: str
    items: List[CartItem] = []
    total: Decimal = Decimal('0.00')
    is_active: bool = True 