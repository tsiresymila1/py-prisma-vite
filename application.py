from pathlib import Path
from starlite import CORSConfig, Starlite, OpenAPIConfig, StaticFilesConfig, TemplateConfig
from starlite.contrib.jinja import JinjaTemplateEngine
from pydantic_openapi_schema.v3_1_0 import Components, SecurityScheme

from routes import web_router, api_router
from ressources import Vite
from database.plugin import PrismaPlugin


prisma_plugin = PrismaPlugin()

template_config = TemplateConfig(
    directory=Path("ressources", "views"),
    engine=JinjaTemplateEngine,
)
template_config.engine_instance.engine.globals['vite'] = Vite.vite

app = Starlite(
    route_handlers=[web_router, api_router],
    plugins=[prisma_plugin],
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
