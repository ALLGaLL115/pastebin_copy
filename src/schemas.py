from pydantic import BaseModel




class CreateMessage(BaseModel):
    name: str
    body: str
    user_id: int

class MessageRead(BaseModel):
    name: str
    messgae_url: str

class MessageUpdate(BaseModel):
    name: str
    body: str

class MessageDB(BaseModel):
    id: int
    name: str
    id_hash: str
    user_id: int 
    message_url: str





from enum import Enum


class Roles(Enum):
    ADMIN = "admin"
    USER = "user"
    UNVERIFICATE = "unverificate"
