


import datetime
from sqlalchemy import delete, or_, select, and_
from models import VerifycationCode
from utils.repository import SqlAlchemyRepository


class VerifycationCodeRepository(SqlAlchemyRepository):
    model = VerifycationCode

    # async def 

    async def verificate(self, code):
        query = select(self.model).where(
            and_(
                self.model.code == code,
                self.model.expiry_time > datetime.datetime.now(datetime.UTC))
        )
        await self.session.execute(query)

    
    

            
    async def delete_unvalid_codes(self):
        query = await delete(self.model).where(
            or_(
            self.model.expiry_time < datetime.now(datetime.UTC)
        ))