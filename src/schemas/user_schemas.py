
from pydantic import BaseModel


class UserDBSchema(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str

class UserReadSchema(BaseModel):
    name: str
    email: str

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str