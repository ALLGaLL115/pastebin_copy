import asyncio
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine,  async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, pool_size = 10)

# async_session_maker = async_sessionmaker(async_engine)s
async_session_maker = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)




async def get_async_session():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass

from sqlalchemy import text, create_engine
engine = create_engine(settings.DATABASE_URL_psycopg2)



