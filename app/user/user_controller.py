
from starlite import Body, Controller, Provide, Request, RequestEncodingType, get, post, put
from prisma.models import User
from typing import Any, Union
from app.user.dto import CreateUserDTO, UpdateUserDTO
from app.user.user_service import UserService


class UserController(Controller):
    path = "/users"
    tags = ['Users']
    security = [{"BearerToken": []}]

    dependencies = {"service": Provide(UserService)}

    @get('/me')
    async def me(self, request: Request[Any,Any],service: UserService) -> Union[User,None]:
        return await service.get_use_by_id(id=request.user.id)
    
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
