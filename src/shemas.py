from pydantic import BaseModel


class UserDB(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str

class UserRead(BaseModel):
    name: str
    email: str

class UserCReate(BaseModel):
    name: str
    email: str
    password: str


class CreateMessage(BaseModel):
    name: str
    body: str

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
    message_url: str
