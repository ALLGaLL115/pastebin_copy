from abc import ABC, abstractmethod
from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
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
        
        stmt =  insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
        
    
    async def get(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.scalar_one()
        # if len(result) <= 1:
        #     return result[0]
        return result
    
    
    async def update(self, filters: dict, data: dict):
        stmt =  update(self.model).filter_by(**filters).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res
    
    
    async def delete(self, **filters):
        stmt =  delete(self.model).filter_by(**filters).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
