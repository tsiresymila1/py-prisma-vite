from pathlib import Path
from starlite import CORSConfig, DefineMiddleware, Starlite, OpenAPIConfig, StaticFilesConfig, TemplateConfig
from starlite.contrib.jinja import JinjaTemplateEngine

from app.auth import login, jwt_auth
from app.user import UserController
from app.spa import SPAController
from ressources import Vite
from pydantic_openapi_schema.v3_1_0 import Components, SecurityScheme
import uvicorn

from database.plugin import PrismaPlugin

prisma_plugin = PrismaPlugin()

template_config = TemplateConfig(
    directory=Path("ressources", "views"),
    engine=JinjaTemplateEngine,
)
template_config.engine_instance.engine.globals['vite'] = Vite.vite

app = Starlite(
    route_handlers=[login, UserController, SPAController],
    plugins=[prisma_plugin],
    middleware=[jwt_auth],
    cors_config=CORSConfig(),
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
        path="/static", directories=[Path("public")])

)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    uvicorn.run("server:app", port=8000, reload=True,
                reload_excludes=["node_modules", "assets"])
