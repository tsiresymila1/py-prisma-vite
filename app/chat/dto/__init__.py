
from pydantic import BaseConfig, BaseModel


class CreateConversationDTO(BaseModel):
    other_id: int
    class Config(BaseConfig):
        arbitrary_types_allowed = True
