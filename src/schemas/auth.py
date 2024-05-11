from pydantic import BaseModel


class SingUpForm(BaseModel):
    name: str
    email: str
    password: str


class Tokenn(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str|None = None