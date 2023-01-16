
from typing import Any
from aiomcache import ValidationException
import bcrypt
from prisma import Prisma
from starlite import ASGIConnection, Body, Controller, Request, RequestEncodingType, Response, Router, post
from starlite.contrib.jwt import Token, JWTAuth
from prisma.models import User
import os


from utils import save_file
from app.auth.dto import LoginDto, RegisterDto


class AuthController(Controller):
    tags = ["Auth"]
    path = "/"

    def __init__(self, owner: "Router") -> None:
        super().__init__(owner)
        self.auth = JWTAuth[User](
            retrieve_user_handler=self.retrieve_user_handler,
            token_secret=os.getenv('JWT_SECRET'),
            exclude=[],
        )

    async def retrieve_user_handler(self, token: Token, connection: ASGIConnection) -> User | None:
        cached_value = await connection.cache.get(token.sub)
        if cached_value:
            return User(**cached_value)
        return None

    @post("/login")
    async def login(self, request: "Request[Any, Any]", data: LoginDto, db: Prisma) -> Response[User]:
        user: User | None = await db.user.find_first(where={
            "email": data.email,
        })
        if user:
            if bcrypt.checkpw(data.password.encode('utf8'), user.password):
                await request.cache.set(str(user.id), user.dict())
                response = self.auth.login(
                    identifier=str(user.id), response_body=user)
                return response
            else:
                raise ValidationException(detail="Password incorrect")
        else:
            raise ValidationException(detail="User not found")

    @post("/register")
    async def register(self, request: "Request[Any, Any]", db: Prisma,data: RegisterDto = Body(media_type=RequestEncodingType.MULTI_PART)) -> dict:
        filename = await save_file(data.profile, encrypted=True)
        return {"filename": filename}
