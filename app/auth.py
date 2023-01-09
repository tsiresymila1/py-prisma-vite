from prisma import Prisma
from starlite.contrib.jwt import JWTAuth, Token
from os import getenv
from typing import Any
from prisma.models import User
from pydantic import BaseModel
import argon2

from starlite import (
    ASGIConnection,
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
    DefineMiddleware,
    Request,
    Response,
    post,
    NotAuthorizedException
)


excludes = ["/schema/*", "/login"]
TOKEN_SECRET = getenv("JWT_SECRET", "abcd123")


class LoginDto(BaseModel):
    email: str
    password: str


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    cached_value = await connection.cache.get(token.sub)
    if cached_value:
        return User(**cached_value)
    return None


auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=TOKEN_SECRET,
    exclude=excludes,
)


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        auth_header = connection.headers.get('Authorization')
        if not connection.url.path.startswith('/api'):
            return AuthenticationResult(user=None, auth=None)
        if not auth_header:
            raise NotAuthorizedException()
        token: Token = Token.decode(encoded_token=auth_header.replace(
            'Bearer ', ''), secret=TOKEN_SECRET, algorithm="HS256")
        cached_value = await connection.cache.get(token.sub)
        if cached_value:
            return AuthenticationResult(user=User(**cached_value), auth=token)
        raise NotAuthorizedException()


jwt_auth = DefineMiddleware(JWTAuthenticationMiddleware, exclude=excludes)


@post("/login", tags=["Auth"])
async def login(request: "Request[Any, Any]", data: LoginDto, db: Prisma) -> Response[User]:
    user: User | None = await db.user.find_first(where={
        "email": data.email,
        "password": data.password  # argon2.argon2_hash(data.password)
    })
    if user:
        await request.cache.set(str(user.id), user.dict())
        response = auth.login(identifier=str(user.id), response_body=user)
        return response
    else:
        raise NotAuthorizedException()
