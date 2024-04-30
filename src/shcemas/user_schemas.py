
from datetime import datetime
from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict


class UserDB(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    verificated: bool
    created_at: datetime

class UserReadSchema(BaseModel):
    name: str
    email: str

class UserCreateSchema(BaseModel):
    
    name: str
    email: str
    password: str