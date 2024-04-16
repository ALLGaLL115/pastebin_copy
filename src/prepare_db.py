# import os
# import sys

# sys.path.append(os.path.join(sys.path[0], 'src'))


from database import async_engine, get_async_session
from schemas import Roles
from models import Role
from sqlalchemy.ext.asyncio import AsyncSession


import asyncio

async def create_roles():
    # получаем текущий цикл событий
    loop = asyncio.get_event_loop()

    async with AsyncSession(async_engine) as session:

        session.add(Role(id = 1, role = Roles.ADMIN.value))
        session.add(Role(id = 2, role = Roles.USER.value))
        session.add(Role(id = 3, role = Roles.UNVERIFICATE.value))

        await session.commit()

if __name__ == '__main__':
    asyncio.run(create_roles())

    
        

