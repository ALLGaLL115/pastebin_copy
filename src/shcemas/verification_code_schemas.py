
from datetime import datetime
from pydantic import BaseModel


class VerifycationCodeDB(BaseModel):
    id: int
    user_id: int
    code: str
    expiry_time: datetime