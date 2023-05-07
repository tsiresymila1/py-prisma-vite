from typing import Any, Optional, Union
import bcrypt
from prisma import Prisma
from prisma.models import User
from app.auth.dto.auth_dto import RegisterDto

from app.user.dto import CreateUserDTO
from utils import hash_pasword, save_file


class UserService:
    _db: Prisma

    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def get_use_by_id(self, id: Union[str,int]) -> Optional[User]:
        return await self._db.user.find_unique(where={"id": id})

    async def get_use_by_email(self, email: str) -> Optional[User]:
        return await self._db.user.find_unique(where={"email": email})

    async def list(self) -> list[User]:
        return await self._db.user.find_many()

    async def create_user(self, data: Union[CreateUserDTO,RegisterDto]) -> User:
        filename = await save_file(data.image, encrypted=True)
        user_data = {
            **data.dict(),
            "image": filename,
            "password": hash_pasword(data.password)
        }
        user: User = await self._db.user.create(user_data)
        return user
