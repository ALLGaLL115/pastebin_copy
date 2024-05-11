import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schemas import UserCreateSchema
from services.auth_service import AuthenticationService, Tokenn, get_password_hash
from api.dependencies import CURUser, UOWDep, get_current_user
from services.user_service import UserService
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, NoResultFound

router = APIRouter(
    tags=['Auth']
)


@router.post("/sing_up")
async def registate_user(uow: UOWDep, new_user: UserCreateSchema):
    res = await AuthenticationService.registration(uow=uow, new_user=new_user)
    return res


@router.post("/send_code")
async def send_code(uow: UOWDep, user_id: int):
    res = await AuthenticationService.send_code(uow=uow, user_id=user_id)
    return res


@router.post("/verification")
async def verificate(uow: UOWDep, code: str, user_id: int):
    res = await AuthenticationService.verification(uow=uow, code=code, user_id=user_id)
    return res


@router.post("/login")
async def login(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    res = await AuthenticationService.login(uow=uow, form_data=form_data)
    return res 


