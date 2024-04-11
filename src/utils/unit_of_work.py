from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.message_repo import MessageRepository
from typing import Type

class IUnitOfWork(ABC):
    messages: Type[MessageRepository]

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplemented
    
    @abstractmethod
    def __aenter__(self, *args):
        raise NotImplemented

    @abstractmethod
    def __aexit__(self):
        raise NotImplemented

    @abstractmethod
    def rollback(self):
        raise NotImplemented
    
    @abstractmethod
    def commit(self):
        raise NotImplemented

 
class UnitOfWork(IUnitOfWork):

    def __init__(self, async_session_maker: AsyncSession) -> None:
        self.session_factory = async_session_maker


    async def __aenter__(self, *args):
        self.sessoin = self.session_factory()
        self.messages(self.sessoin)
        return self
    
    async def __aexit__(self):
       await  self.rollback()
       await self.sessoin.close()
        
    async def rollback(self):
        await self.session.rollback()
      
    async def commit(self):
        await self.session.commit()