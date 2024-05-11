import asyncio
import os
import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from httpx import ASGITransport, AsyncClient
from main import app
from fastapi.testclient import TestClient
from typing import AsyncGenerator, AsyncIterator
from database import Base
from models import *
import threading
import asyncio


engine = create_async_engine(settings.DATABASE_URL_asyncpg)

session_maker = async_sessionmaker(engine, expire_on_commit=False, future=True, echo=False)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.DATABASE_URL_asyncpg.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE user_id = $1;""", user_id
            )

    return get_user_from_database_by_uuid

# @pytest.fixture(scope='session')
# async def create_user(asyncpg_pool):
#     async with asyncpg_pool.acquire() as connection:
#         stmt = insert(User).values(
#             name="1",
#             email="alihannn5@mail.ru",
#             password="1"

#         )
#         res = await connection.fetch(stmt)
#         print(res)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)        
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session", autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient( transport=ASGITransport(app=app), base_url="https://test") as ac:
        yield ac


