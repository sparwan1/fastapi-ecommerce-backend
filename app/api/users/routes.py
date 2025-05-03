from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.mongodb import mongodb
from app.db.repositories.user import UserRepository
from app.db.repositories.cart import CartRepository
from app.schemas.user import UserCreate, UserPut, UserPatch, UserInDB, user_helper
from app.core.security import get_password_hash

router = APIRouter()

async def get_user_repository():
    return UserRepository(mongodb.db.users)

async def get_cart_repository():
    return CartRepository(mongodb.db.carts)

@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
    cart_repo: CartRepository = Depends(get_cart_repository)
):
    # Check if user exists
    if await user_repo.find_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if await user_repo.find_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_data.password)
    del user_dict["password"]
    user_dict["is_active"] = True
    user_dict["is_superuser"] = False
    
    user = await user_repo.create(user_dict)
    
    # Create cart for user
    await cart_repo.create({"user_id": str(user["_id"]), "items": [], "total": 0})
    return user_helper(user)

@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    user = await user_repo.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_helper(user)

@router.get("/", response_model=List[UserInDB])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    user_repo: UserRepository = Depends(get_user_repository)
):
    users = await user_repo.find_all(skip=skip, limit=limit)
    return [user_helper(u) for u in users]

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: str,
    user_data: UserPut,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check for unique username/email (allow if it's the same as current user)
    if user_data.username != user["username"]:
        if await user_repo.find_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    if user_data.email != user["email"]:
        if await user_repo.find_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    update_data = user_data.model_dump()
    update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    updated_user = await user_repo.update(user_id, update_data)
    return user_helper(updated_user)

@router.patch("/{user_id}", response_model=UserInDB)
async def partial_update_user(
    user_id: str,
    user_data: UserPatch,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_data.model_dump(exclude_unset=True)

    # Only username and full_name can be updated
    if "username" in update_data and update_data["username"] != user["username"]:
        if await user_repo.find_by_username(update_data["username"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    # Email cannot be updated via PATCH

    updated_user = await user_repo.update(user_id, update_data)
    return user_helper(updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_repo: UserRepository = Depends(get_user_repository),
    cart_repo: CartRepository = Depends(get_cart_repository)
):
    user = await user_repo.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user's cart
    cart = await cart_repo.find_by_user_id(user_id)
    if cart:
        await cart_repo.delete(str(cart["_id"]))

    # Delete user
    await user_repo.delete(user_id) 