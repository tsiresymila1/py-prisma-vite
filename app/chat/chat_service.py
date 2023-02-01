from prisma import Prisma
from prisma.models import Conversation, User


class ChatService:

    _db: Prisma

    def __init__(self, db: Prisma):
        self._db = db

    def list_chat(self, user_id: int) -> list[Conversation]:
        user: User | None = self._db.user.find_first(whare={
            "id": user_id,
        }, include=["conversations"])
        if user and user.conversations:
            return user.conversations
        return []
