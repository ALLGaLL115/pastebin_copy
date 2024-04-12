from config import settings
from sqlalchemy.ext.asyncio import create_async_engine,  async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)

async_session_maker = async_sessionmaker(async_engine)



async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass