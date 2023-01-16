from prisma import Prisma
from prisma.models import User
from starlite import Controller, Provide, get, post, put
from typing import Any

from app.user.dto import CreateUserDTO, UpdateUserDTO
from app.user.user_service import UserService


class UserController(Controller):
    path = "/users"
    tags = ['Users']
    security=[{"BearerToken": []}]

    dependencies ={"service": Provide(UserService)}

    @get()
    async def get(self, service: UserService) -> list[User]:
        return await service.list()

    @post()
    def create(self, data: CreateUserDTO) -> dict[str, Any]:
        return data

    @put('/:id')
    def update(self, id: int,data: UpdateUserDTO) -> dict[str, Any]:
        return data
