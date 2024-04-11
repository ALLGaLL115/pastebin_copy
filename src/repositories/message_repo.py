from utils.repository import SqlAlchemyRepository
from models import Message

class MessageRepository(SqlAlchemyRepository):
    model = Message