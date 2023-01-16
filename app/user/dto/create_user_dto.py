from pydantic import BaseModel
from pydantic_partial import create_partial_model


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password:  str

UpdateUserDTO = create_partial_model(CreateUserDTO,"UpdateUserDTO")