from pydantic import BaseConfig, BaseModel
from prisma.enums import Role
from starlite import UploadFile


class LoginDto(BaseModel):
    email: str
    password: str


class RegisterDto(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: Role
    image: UploadFile

    class Config(BaseConfig):
        arbitrary_types_allowed = True
