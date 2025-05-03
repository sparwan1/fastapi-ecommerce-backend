from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ProductInDB(ProductBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True

class ProductPatch(BaseModel):
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    image_url: Optional[str] = None

def product_helper(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "stock": product["stock"],
        "category": product["category"],
        "image_url": product.get("image_url"),
        "is_active": product.get("is_active", True),
    } 