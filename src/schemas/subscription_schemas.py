  
# from models import User
from pydantic import BaseModel




class SubscriptionDB(BaseModel):
    subscriber_id: int
    target_id: int
   