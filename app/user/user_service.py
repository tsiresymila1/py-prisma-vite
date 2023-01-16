from typing import Optional
from prisma import Prisma
from prisma.models import User


class UserService:
    _db: Prisma

    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def get_use_by_id(self, id: str | int) -> Optional[User]:
        return await self._db.user.find_unique(where={"id": id})

    async def list(self) -> list[User]:
        return await self._db.user.find_many()
