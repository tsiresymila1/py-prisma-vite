from starlite import Router
from app.auth import JWTAuthenticationMiddleware
from app.user import UserController

api_router = Router( 
    path="/api",
    route_handlers=[UserController], 
    middleware=[JWTAuthenticationMiddleware],
)
