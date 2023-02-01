
from pydantic import BaseConfig, BaseModel


class CreateConversationDTO(BaseModel):
    ids: list[int]
    class Config(BaseConfig):
        arbitrary_types_allowed = True
