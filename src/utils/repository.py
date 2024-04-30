from abc import ABC, abstractmethod
from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete, or_
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplemented
    
    @abstractmethod
    async def get():
        raise NotImplemented
    
    @abstractmethod
    async def update():
        raise NotImplemented
    
    @abstractmethod
    async def delete():
        raise NotImplemented
    



class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **data):
        
        stmt =  insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        result = result.scalar_one()
        return result.convert_to_model()
        
    
    async def get(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        # if len(result) <= 1:
        #     return result[0]
        return result.convert_to_model()
    
    async def get_count(self, **filters):
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        response = await self.session.execute(stmt)
        return  response.scalar()
        
    
    
    async def get_all(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        result = [row.convert_to_model() for row in result]
        return result
   
    
    async def get_all_or(self, **kwargs):
        d = []
        stmt = select(self.model).filter_by(or_(kwargs))
        stmt = select().where()
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        return result

    
    
    async def update(self, data: dict, **filters):
        stmt =  update(self.model).filter_by(**filters).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res.convert_to_model()
    
    
    async def delete(self, **filters):
        stmt =  delete(self.model).filter_by(**filters).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
