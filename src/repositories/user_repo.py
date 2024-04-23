import logging

from fastapi import HTTPException
from sqlalchemy import select
from models import User
from utils.repository import SqlAlchemyRepository

class UserRepository(SqlAlchemyRepository):
    model = User 


    async def check_verification(self, filters: dict)->bool:
        try:
            query = select(self.model.role).filter_by(**filters)

            role = await self.session.execute(query)
            role = role.scalar_one()

            if role == 3:
                return False
            
            return True
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=500)
