from typing import Any
from starlite import Controller, Provide, Request, get, post
from prisma.models import Conversation

from app.chat.chat_service import ChatService
from app.chat.dto import CreateConversationDTO
from app.message.message_service import MessageService


class ChatController(Controller):

    path = "/chat"
    tags = ['Chats']
    security = [{"BearerToken": []}]

    dependencies = {
        "message_service": Provide(MessageService),
        "service": Provide(ChatService)
    }

    @get()
    async def chat(self, request: Request, service: ChatService) -> list[Conversation]:
        return await service.list_chat(request.user.id)

    @post('')
    async def find(self, service: ChatService, data: CreateConversationDTO, request: Request[Any, Any]) -> Conversation:
        conversation: Conversation = await service.find_conversation(request.user, data.ids)
        return conversation
