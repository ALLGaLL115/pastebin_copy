import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.dependencies import UOWDep
from config import settings
from conftest import session_maker
from httpx import AsyncClient
import pytest
import pytest_asyncio
from models import VerifycationCode
from  schemas.auth import SingUpForm
from schemas.user_schemas import UserDB
from services.verification_service import VerificationCodeService, generate_verification_code






modelka = SingUpForm(
    name="1",
    email="alihannn5@mail.ru",
    password="1"
)

class A:
    id: str
    name: str
    email: str
    password: str
    


async def test_sing_up(ac: AsyncClient, get_user_from_database):
    response = await ac.post(url=f"{settings.APP_HOST}/sing_up", json=modelka.model_dump())
    data = modelka.model_dump()
    data["id"] = response.json()["user_id"]
    assert response.json()['status'] == "succes"
    res = await get_user_from_database(1)
    print(res)

# async def test_send_code(ac: AsyncClient, user_id: int = 1):
#     response = await ac.post(url=f"{settings.APP_HOST}/sing_up", json=modelka.model_dump())
#     print(response.json())


#     response = await ac.post(url=f"{settings.APP_HOST}/send_code?user_id={user_id}")
   
#     print(response.json())
#     assert response.json()["message"] == "succes"


# @pytest.mark.usefixtures()
# async def test_verification(ac: AsyncClient, ):
#     response = await ac.post(url=f"{settings.APP_HOST}/sing_up", json={
#         "name":"2",
#         "email":"2lihannn5@mail.ru",
#         "password":"2"
#     })
#     assert response.json()['status'] == "succes"
#     user_id = response.json()["user_id"]
#     response = await ac.post(url=f"{settings.APP_HOST}/send_code?user_id={user_id}")
#     assert 1==1
    # async with uow:
    #     result = await uow.verification_codes.get(user_id=user_id)
    #     print(result)




# async def test_login(ac: AsyncClient, username: str, password: str):
#     response = await ac.post(
#         url=f"{settings.APP_HOST}/login",
#         headers={
#             'accept': 'application/json',
#             'Content-Type': 'application/x-www-form-urlencoded'
#         },
#         data = {
#             'grant_type': '',
#             'username': username,
#             'password': password,
#             'scope': '',
#             'client_id': '',
#             'client_secret': ''
#         })
#     assert 1==1
    