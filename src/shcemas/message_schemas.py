from pydantic import BaseModel

class CreateMessage(BaseModel):
    name: str
    body: str


class MessageRead(BaseModel):
    name: str
    messgae_url: str


class MessageUpdate(BaseModel):
    name: str|None = None
    body: str|None = None


class MessageDB(BaseModel):
    id: int
    name: str
    hash_id: str
    user_id: int 
    message_url: str
