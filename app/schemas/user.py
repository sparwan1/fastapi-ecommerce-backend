from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# For PUT: all fields required
class UserPut(UserBase):
    password: str = Field(..., min_length=8)

# For PATCH: only username and full_name allowed, both optional
class UserPatch(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserInDB(UserBase):
    id: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

def user_helper(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "is_active": user.get("is_active", True),
        "is_superuser": user.get("is_superuser", False),
    } 