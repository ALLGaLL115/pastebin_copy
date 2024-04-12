from abc import ABC, abstractmethod

import aioredis
from database import async_session_maker
from repositories.message_repo import MessageRepository
from typing import Type

class IUnitOfWork(ABC):
    redis: Type[aioredis.Redis]

    messages: Type[MessageRepository]


    @abstractmethod
    def __init__(self) -> None:
        raise NotImplemented
    
    @abstractmethod
    def __aenter__(self):
        raise NotImplemented

    @abstractmethod
    def __aexit__(self, *args):
        raise NotImplemented

    @abstractmethod
    def rollback(self):
        raise NotImplemented
    
    @abstractmethod
    def commit(self):
        raise NotImplemented

 
# class UnitOfWork(IUnitOfWork):

    # def __init__(self):
    #     self.session_factory = async_session_maker
    #     self.pool = aioredis.ConnectionsPool("redis://localhost", minsize=0, maxsize=200)
    #     self.redis = aioredis.Redis(self.pool)




    # async def __aenter__(self):
    #     self.session = self.session_factory()
    #     self.messages(self.session)
    #     return self
    
    # async def __aexit__(self, *args):
    #    await  self.rollback()
    #    await self.redis.close()
    #    await self.session.close()
        
    # async def rollback(self):
    #     await self.session.rollback()
      
    # async def commit(self):
    #     await self.session.commit()


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker
        self.pool = aioredis.ConnectionsPool("redis://localhost", minsize=0, maxsize=200)
        self.redis = aioredis.Redis(self.pool)


    async def __aenter__(self):
        self.session = self.session_factory()
        self.messages(self.session)
      
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()
      
    async def commit(self):
        await self.session.commit()
        




