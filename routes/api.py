from starlite import Router
from app.auth.auth_controller import AuthController
from app.auth.middleware import jwt_auth
from app.chat import ChatController
from app.message.message_controller import MessageController
from app.user import UserController

api_router = Router(
    path="/api",
    route_handlers=[AuthController, UserController,
                    ChatController, MessageController],
    middleware=[jwt_auth],
)
