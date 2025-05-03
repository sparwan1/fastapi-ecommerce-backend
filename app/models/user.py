from typing import Optional
from app.models.base import BaseDBModel

class User(BaseDBModel):
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False 