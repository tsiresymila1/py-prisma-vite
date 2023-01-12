from pathlib import Path
from typing import Any
from starlite import CORSConfig, Request, Response, Starlite, OpenAPIConfig, StaticFilesConfig, TemplateConfig, HttpMethod
from starlite.response import RedirectResponse
from starlite.status_codes import HTTP_405_METHOD_NOT_ALLOWED
from starlite.exceptions import MethodNotAllowedException

from starlite.contrib.jinja import JinjaTemplateEngine
from pydantic_openapi_schema.v3_1_0 import Components, SecurityScheme

from modules import SocketManager

from routes import web_router, api_router
from ressources import Vite
from database.plugin import PrismaPlugin


prisma_plugin = PrismaPlugin()

template_config = TemplateConfig(
    directory=Path("ressources", "views"),
    engine=JinjaTemplateEngine,
)
template_config.engine_instance.engine.globals['vite'] = Vite.vite


def handle_method_not_allowed(request: Request, exc: MethodNotAllowedException) -> Response:
    if request.method == HttpMethod.GET:
        return RedirectResponse(url="/")
    return Response(content={"detail": exc.detail, "status_code": exc.status_code}, status_code=exc.status_code)


startite_app = Starlite(
    route_handlers=[web_router, api_router],
    plugins=[prisma_plugin],
    cors_config=CORSConfig(),
    exception_handlers={
        HTTP_405_METHOD_NOT_ALLOWED: handle_method_not_allowed
    },
    openapi_config=OpenAPIConfig(
        title="WEBSEC API",
        version="1.0.0",
        components=Components(
            securitySchemes={
                "BearerToken": SecurityScheme(
                    type="http",
                    scheme="bearer",
                )
            },
        ),),
    template_config=template_config,
    debug=True,
    static_files_config=StaticFilesConfig(
        path="/static", directories=[Path("public/static")])

)

io = SocketManager(app=startite_app)
app = io.get_asgi_app()


@io.on("connect")
def connect(sid: Any, environ: Any):
    print("Client connected : ", sid, environ)

@io.on('message')
async def message(sid: Any,data: Any):
    print("message : ",sid,data)
    await io.emit('message', {"response": "ok"})   

@io.on("disconnect")
def disconnect(sid: Any):
    print("Client disconnect : ", sid)
