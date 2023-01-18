from starlite import ASGIConnection, AbstractAuthenticationMiddleware, AuthenticationResult, DefineMiddleware, NotAuthorizedException
from starlite.contrib.jwt import Token
from prisma.models import User
import os


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        auth_header = connection.headers.get('Authorization')
        if not auth_header:
            raise NotAuthorizedException()
        token: Token = Token.decode(encoded_token=auth_header.replace(
            'Bearer ', ''), secret=os.getenv("JWT_SECRET", "abcd123"), algorithm="HS256")
        cached_value = await connection.cache.get(token.sub)
        if cached_value:
            return AuthenticationResult(user=User(**cached_value), auth=token)
        raise NotAuthorizedException()


jwt_auth = DefineMiddleware(JWTAuthenticationMiddleware, exclude=["/api/auth/login","/api/auth/register"])
