from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.db.mongodb import mongodb
from app.db.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB, ProductPatch, product_helper

router = APIRouter()

async def get_product_repository():
    return ProductRepository(mongodb.db.products)

@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    product_dict = product_data.model_dump()
    product_dict["price"] = float(product_dict["price"])
    product_dict["is_active"] = True
    product = await product_repo.create(product_dict)
    return product_helper(product)

@router.get("/{product_id}", response_model=ProductInDB)
async def get_product(
    product_id: str,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    try:
        product = await product_repo.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid product id format"
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product_helper(product)

@router.get("/", response_model=List[ProductInDB])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    query = {}
    if category:
        query["category"] = category
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    products = await product_repo.find_all(query, skip=skip, limit=limit)
    from app.schemas.product import product_helper
    return [product_helper(p) for p in products]

@router.put("/{product_id}", response_model=ProductInDB)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    try:
        product = await product_repo.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product id format"
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    # Convert Decimal to float if needed
    if "price" in update_data:
        update_data["price"] = float(update_data["price"])
    updated_product = await product_repo.update(str(product["_id"]), update_data)
    return product_helper(updated_product)

@router.patch("/{product_id}", response_model=ProductInDB)
async def partial_update_product(
    product_id: str,
    product_data: ProductPatch,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    try:
        product = await product_repo.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product id format"
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)

    # Only allow updates to price, stock, description, image_url
    allowed_fields = {"price", "stock", "description", "image_url"}
    update_data = {k: v for k, v in update_data.items() if k in allowed_fields}

    # Convert Decimal to float for price if present
    if "price" in update_data:
        update_data["price"] = float(update_data["price"])

    updated_product = await product_repo.update(str(product["_id"]), update_data)
    return product_helper(updated_product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    product_repo: ProductRepository = Depends(get_product_repository)
):
    try:
        product = await product_repo.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product id format"
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    await product_repo.delete(str(product["_id"])) 