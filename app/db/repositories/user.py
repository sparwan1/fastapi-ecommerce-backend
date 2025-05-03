from typing import Optional
from app.db.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    async def find_by_email(self, email: str) -> Optional[dict]:
        return await self.find_one({"email": email})

    async def find_by_username(self, username: str) -> Optional[dict]:
        return await self.find_one({"username": username}) 