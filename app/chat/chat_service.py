from prisma import Prisma
from prisma.models import Conversation, User

from app.message.message_service import MessageService


class ChatService:

    _db: Prisma
    _message_service: MessageService

    def __init__(self, db: Prisma, message_service: MessageService):
        self._db = db
        self._message_service = message_service

    async def list_chat(self, user_id: int) -> list[Conversation]:
        user: User | None = await self._db.user.find_first(
            where={
                "id": user_id,
            }, include={
                "conversations": {
                    "include": {
                        "messages": {
                            "take": 1,
                            "order_by": {
                                "createdAt": "desc",
                            },
                            "include": {
                                "readers": True
                            }

                        }
                    }

                }

            })
        if user and user.conversations:
            return user.conversations
        return []

    async def create_chat(self, user: User, ids: list[int]) -> Conversation:
        conversation: Conversation = await self._db.conversation.create(
            data={
                "participants": {
                    'connect': [{"id": user.id}]+[{"id": id} for id in ids]
                },
                "initiator": {
                    "connect": {
                        "id": user.id
                    }
                }
            },
            include={
                "participants": True,
                "messages": {
                    "include": {
                        "readers": True
                    }
                }
            }
        )
        return conversation

    async def find_conversation(self, user: User, ids: list[int]) -> Conversation:
        conversation:  Conversation | None = await self._db.conversation.find_first(
            where={
                "AND": [{"participants": {"some": {"id": user.id}}}] + [{"participants": {"some": {"id": id}}} for id in ids]
            },
            include={
                "participants": True,
                "messages": {
                    "include": {
                        "readers": True
                    }
                }
            }
        )
        if not conversation:
            return await self.create_chat(user, ids)

        for message in conversation.messages:
            readers: list[int] = [r.id for r in message.readers]
            if user.id not in readers:
                await self._message_service.read(user.id, message.id)
        return conversation
