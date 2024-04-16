from models import User
from utils.repository import SqlAlchemyRepository

class UserRepository(SqlAlchemyRepository):
    model = User 