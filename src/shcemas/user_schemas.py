
from datetime import datetime
from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict


class UserDBSchema(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    role: int
    created_at: datetime

class UserReadSchema(BaseModel):
    name: str
    email: str

class UserCreateSchema(BaseModel):
    
    name: str
    email: str
    password: str