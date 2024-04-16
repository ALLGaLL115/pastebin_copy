from abc import ABC, abstractmethod
from database import async_session_maker
from repositories.message_repo import MessageRepository
from typing import Type

from repositories.user_repo import UserRepository

class IUnitOfWork(ABC):

    users: Type[UserRepository]
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



class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker


    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.messages = MessageRepository(self.session)
      
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
        
    async def rollback(self):
        await self.session.rollback()
        
      




