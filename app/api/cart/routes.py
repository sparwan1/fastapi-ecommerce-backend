from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import mongodb
from app.db.repositories.cart import CartRepository
from app.db.repositories.product import ProductRepository
from app.db.repositories.user import UserRepository
from app.schemas.cart import CartCreate, CartUpdate, CartInDB, CartItemCreate, cart_helper

router = APIRouter()

async def get_cart_repository():
    return CartRepository(mongodb.db.carts)

async def get_product_repository():
    return ProductRepository(mongodb.db.products)

async def get_user_repository():
    return UserRepository(mongodb.db.users)

@router.post("/", response_model=CartInDB, status_code=status.HTTP_201_CREATED)
async def create_cart(
    cart_data: CartCreate,
    cart_repo: CartRepository = Depends(get_cart_repository),
    user_repo: UserRepository = Depends(get_user_repository)
):
    user_id = str(cart_data.user_id)

    # 1. Check if user exists
    user = await user_repo.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # 2. Check if user already has a cart
    existing_cart = await cart_repo.find_by_user_id(user_id)
    if existing_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active cart"
        )

    # 3. Create the cart
    cart_dict = cart_data.model_dump()
    cart_dict["user_id"] = user_id
    if "total" in cart_dict:
        cart_dict["total"] = float(cart_dict["total"])
    cart = await cart_repo.create(cart_dict)
    return cart_helper(cart)

@router.get("/{cart_id}", response_model=CartInDB)
async def get_cart(
    cart_id: str,
    cart_repo: CartRepository = Depends(get_cart_repository)
):
    try:
        cart = await cart_repo.find_one({"_id": ObjectId(cart_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cart id format"
        )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    return cart_helper(cart)

@router.post("/{cart_id}/items", response_model=CartInDB)
async def add_item_to_cart(
    cart_id: str,
    item_data: CartItemCreate,
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: ProductRepository = Depends(get_product_repository)
):
    # Convert cart_id to ObjectId
    try:
        cart = await cart_repo.find_one({"_id": ObjectId(cart_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cart id format"
        )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    # Convert product_id to ObjectId
    try:
        product = await product_repo.find_one({"_id": ObjectId(item_data.product_id)})
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
    if product["stock"] < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock"
        )

    # Calculate price
    item_price = float(product["price"]) * item_data.quantity

    # Build the cart item
    cart_item = {
        "id": str(ObjectId()),
        "product_id": item_data.product_id,
        "quantity": item_data.quantity,
        "price": float(product["price"])
    }

    # Add item to cart
    updated_cart = await cart_repo.add_item(cart_id, cart_item)
    if not updated_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add item to cart"
        )

    # Update product stock
    await product_repo.update_stock(item_data.product_id, item_data.quantity)
    return cart_helper(updated_cart)

@router.delete("/{cart_id}/items/{item_id}", response_model=CartInDB)
async def remove_item_from_cart(
    cart_id: str,
    item_id: str,
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: ProductRepository = Depends(get_product_repository)
):
    # Check if cart exists
    cart = await cart_repo.find_one({"_id": ObjectId(cart_id)})
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    # Remove item from cart
    updated_cart = await cart_repo.remove_item(cart_id, item_id)
    if not updated_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not remove item from cart"
        )

    return cart_helper(updated_cart)

@router.delete("/{cart_id}/clear", response_model=CartInDB)
async def clear_cart(
    cart_id: str,
    cart_repo: CartRepository = Depends(get_cart_repository)
):
    # Check if cart exists
    cart = await cart_repo.find_one({"_id": ObjectId(cart_id)})
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    # Clear cart
    updated_cart = await cart_repo.clear_cart(cart_id)
    if not updated_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not clear cart"
        )

    return cart_helper(updated_cart)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: str,
    cart_repo: CartRepository = Depends(get_cart_repository)
):
    try:
        cart = await cart_repo.find_one({"_id": ObjectId(cart_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cart id format"
        )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    await cart_repo.delete(str(cart["_id"])) 