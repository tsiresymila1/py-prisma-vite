from prisma import Prisma
from prisma.models import Message, User
from prisma.enums import MessageType

from app.message.dto import CreateMessageDTO
from utils import save_file


class MessageService:
    _db: Prisma

    def __init__(self, db: Prisma):
        self._db = db

    async def _send_message(self, user_id, conversation_id, content, messsage_type: MessageType) -> Message:
        message: Message = await self._db.message.create(
            data={
                "content": content,
                "type": messsage_type,
                "user": {
                    "connect": {
                        "id": user_id
                    }
                },
                "conversation": {
                    "connect": {
                        "id": conversation_id
                    }
                },
                "readers": {
                    "connect": [{"id": user_id}]
                }
            },
            include={"readers": True}
        )
        return message

    async def send(self, user: User, data: CreateMessageDTO) -> list[Message]:
        messages = []
        if data.content != "":
            message: Message = await self._send_message(user.id, data.conversation_id, data.content, MessageType.String)
            messages.append(message)
        if data.files:
            for file in data.files:
                filename = await save_file(file, encrypted=True)
                message: Message = await self._send_message(user.id, data.conversation_id, filename, MessageType.File)
                messages.append(message)
        return messages

    async def read(self, user: User, id: int) -> Message:
        await self._db.message.update_many(
            data={
                "readers": {
                    "connect": {"id": user.id}
                }
            },
            where={
                "conversationId": id
            }
        )
