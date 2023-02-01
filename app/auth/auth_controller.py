from typing import Any
from aiomcache import ValidationException
import bcrypt
from starlite import ASGIConnection, Body, Controller, Provide, Request, RequestEncodingType, Response, Router, post
from starlite.contrib.jwt import Token, JWTAuth
from prisma.models import User
import os
from datetime import timedelta

from app.user.user_service import UserService
from app.auth.dto import LoginDto, RegisterDto


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    cached_value = await connection.cache.get(token.sub)
    if cached_value:
        return User(**cached_value)
    return None


class AuthController(Controller):
    tags = ["Auth"]
    path = "/auth"

    dependencies = {"service": Provide(UserService)}

    def __init__(self, owner: "Router") -> None:
        super().__init__(owner)
        self.auth = JWTAuth[User](
            retrieve_user_handler=retrieve_user_handler,
            token_secret=os.getenv('JWT_SECRET', 'adbcdabdcd'),
            exclude=[],
        )

    @post("/login")
    async def login(self, service: UserService, request: "Request[Any, Any]",
                    data: LoginDto = Body(media_type=RequestEncodingType.JSON)) -> Response[User]:
        user: User | None = await service.get_use_by_email(data.email)
        if user:
            p = user.password.encode('utf8')
            try:
                is_verify_password = bcrypt.checkpw(
                    data.password.encode('utf8'), p)
                if is_verify_password:
                    await request.cache.set(str(user.id), user.dict())
                    response = self.auth.login(
                        token_expiration=timedelta(days=1),
                        identifier=str(user.id), response_body=user)
                    return response
                else:
                    raise ValidationException(msg="Password incorrect")
            except Exception:
                raise ValidationException(msg="Password incorrect")
        else:
            raise ValidationException(msg="User not found")

    @post("/register")
    async def register(self, service: UserService,request: "Request[Any, Any]",
                       data: RegisterDto = Body(media_type=RequestEncodingType.MULTI_PART)) -> Response[dict]:
        user: dict = await service.create_user(data)
        await request.cache.set(str(user.id), user.dict())
        response = self.auth.login(
            token_expiration=timedelta(days=1),
            identifier=str(user.id), response_body=user)
        return response
