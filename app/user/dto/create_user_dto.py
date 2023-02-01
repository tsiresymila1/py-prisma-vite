from pydantic import BaseConfig, BaseModel
from pydantic_partial import create_partial_model
from prisma.enums import Role
from starlite import UploadFile


class CreateUserDTO(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: Role
    image: UploadFile

    class Config(BaseConfig):
        arbitrary_types_allowed = True


UpdateUserDTO = create_partial_model(CreateUserDTO)
