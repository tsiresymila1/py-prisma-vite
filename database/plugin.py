from typing import Any
from prisma import Prisma
from starlite import PluginProtocol, Provide, Request, Response, Starlite


class PrismaPlugin(PluginProtocol[Any]):
    _db: Prisma

    def __init__(self) -> None:

        super().__init__()
        self._db = Prisma()

    async def start(self, _: Request) -> None:
        print("DB initialized ")
        await self._db.disconnect()
        await self._db.connect()

    async def stop(self, _: Response) -> Response:
        await self._db.disconnect()
        return _

    def getDB(self) -> Prisma:
        return self._db

    def on_app_init(self, app: Starlite) -> None:
        app.dependencies.update({"db": Provide(self.getDB)})
        app.on_startup = [self.start]
        app.on_shutdown = [self.stop]
        return super().on_app_init(app)
