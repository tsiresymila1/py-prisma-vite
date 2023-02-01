from typing import Any
from starlite import Controller, Provide, Request, get, post
from prisma.models import Conversation

from app.chat.chat_service import ChatService
from app.chat.dto import CreateConversationDTO


class ChatController(Controller):

    path = "/chat"
    tags = ['Chats']
    security = [{"BearerToken": []}]

    dependencies = {"service": Provide(ChatService)}

    @get()
    def chat(self, request: Request, service: ChatService) -> list[Conversation]:
        return service.list_chat(request.user.id)

    @post()
    def create(self, data: CreateConversationDTO, request: Request[Any, Any]) -> None:
        ...
