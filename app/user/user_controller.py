
from starlite import Body, Controller, Provide, RequestEncodingType, get, post, put
from typing import Any
from app.user.dto import CreateUserDTO, UpdateUserDTO
from app.user.user_service import UserService


class UserController(Controller):
    path = "/users"
    tags = ['Users']
    security = [{"BearerToken": []}]

    dependencies = {"service": Provide(UserService)}

    @get()
    async def get(self, service: UserService) -> list[dict[str,Any]]:
        users = await service.list()
        return [u.dict() for u in users]

    @post()
    async def create(self, service: UserService, data: CreateUserDTO = Body(media_type=RequestEncodingType.MULTI_PART)) -> dict[str, Any]:
        return  await service.create_user(data=data)

    @put("/{id:int}")
    def update(self, id: int, data: UpdateUserDTO = Body(media_type=RequestEncodingType.MULTI_PART)) -> dict[str, Any]:
        return data.dict()
