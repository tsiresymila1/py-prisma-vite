from prisma import Prisma
from prisma.models import User
from starlite import Controller, get, post
from typing import Any

from app.user.dto import CreateUserDTO


class UserController(Controller):
    path = "/api/users"
    tags = ['Users']
    security=[{"BearerToken": []}]

    @get()
    def get(self, db: Prisma) -> list[User]:
        return db.user.find_many()  

    @post()
    def create(self, data: CreateUserDTO) -> dict[str, Any]:
        return data
