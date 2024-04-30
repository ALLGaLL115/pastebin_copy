


import datetime
from sqlalchemy import delete, or_, select, and_
from models import VerifycationCode
from utils.repository import SqlAlchemyRepository


class VerifycationCodeRepository(SqlAlchemyRepository):
    model = VerifycationCode


    async def get_valid_user_code(self, user_id)-> VerifycationCode|None:
        now = datetime.datetime.now(datetime.UTC)
        query = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.expiry_time > now)
        )
        res = await self.session.execute(query)
        res = res.scalar()
        
        return res
    

    async def validate_code(self, code:str, user_id:int ):
        now = datetime.datetime.now(datetime.timezone.utc)
        query = select(self.model).where(
            and_(
            self.model.code == code,
            self.model.user_id == user_id,
            self.model.expiry_time > now)
        )
        res = await self.session.execute(query)
        res = res.scalar_one()

            
    async def delete_unvalid_codes(self):
        query = await delete(self.model).where(
            or_(
            self.model.expiry_time < datetime.now(datetime.UTC)
        ))