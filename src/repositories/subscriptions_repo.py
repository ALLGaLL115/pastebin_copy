from models import Subscription
from utils.repository import SqlAlchemyRepository



class SubscriptionsRepository(SqlAlchemyRepository):
    model = Subscription

