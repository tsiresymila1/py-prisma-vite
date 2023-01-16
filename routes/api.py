from starlite import Router
from app.auth.middleware import jwt_auth
from app.user import UserController

api_router = Router( 
    path="/api",
    route_handlers=[UserController], 
    middleware=[jwt_auth],
)
