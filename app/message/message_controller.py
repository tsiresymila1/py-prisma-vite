from prisma.models import Message
from starlite import Body, Controller, Provide, Request, RequestEncodingType, post
from app.message.dto import CreateMessageDTO

from app.message.message_service import MessageService


class MessageController(Controller):

    path = "/message"
    tags = ['Messages']
    security = [{"BearerToken": []}]

    dependencies = {"service": Provide(MessageService)}

    @post("/send")
    async def send(self, request: Request, service: MessageService, data: CreateMessageDTO = Body(media_type=RequestEncodingType.MULTI_PART)) -> list[Message]:
        return await service.send(request.user, data)
