from typing import Optional
from pydantic import BaseConfig, BaseModel
from prisma.enums import MessageType
from starlite import  UploadFile


class CreateMessageDTO(BaseModel):
    conversation_id: int
    content: Optional[str]
    files: Optional[list[UploadFile]]

    class Config(BaseConfig):
        arbitrary_types_allowed = True
