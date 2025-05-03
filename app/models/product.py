from typing import Optional
from decimal import Decimal
from app.models.base import BaseDBModel

class Product(BaseDBModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    image_url: Optional[str] = None
    is_active: bool = True 