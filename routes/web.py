
from starlite import Router
from app.spa import SPAController

web_router = Router(path="/", route_handlers=[SPAController],)

