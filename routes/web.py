
from starlite import Router
from app.auth import AuthController
from app.spa import SPAController

web_router = Router(path="/", route_handlers=[AuthController, SPAController],)

