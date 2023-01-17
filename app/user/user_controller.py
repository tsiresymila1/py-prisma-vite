from prisma import Prisma
from prisma.models import User
from starlite import Body, Controller, Provide, RequestEncodingType, Response, get, post, put
from typing import Any

from app.user.dto import CreateUserDTO, UpdateUserDTO
from app.user.user_service import UserService


class UserController(Controller):
    path = "/users"
    tags = ['Users']
    security = [{"BearerToken": []}]

    dependencies = {"service": Provide(UserService)}

    @get()
    async def get(self, service: UserService) -> list[User]:
        return await service.list()

    @post()
    async def create(self, service: UserService, data: CreateUserDTO = Body(media_type=RequestEncodingType.MULTI_PART)) -> dict[str, Any]:
        return  await service.create_user(data=data)

    @put("/{id:int}")
    def update(self, id: int, data: UpdateUserDTO = Body(media_type=RequestEncodingType.MULTI_PART)) -> dict[str, Any]:
        return data.dict()
