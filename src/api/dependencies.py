import logging
from fastapi import Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from models import User
from shcemas.user_schemas import UserDB
from utils.unit_of_work import IUnitOfWork, UnitOfWork
from jose import jwt, JWTError
from config import settings
from fastapi.requests import Request

UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]


def get_redis(request: Request):
    return request.state.redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(uow: UOWDep, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    async with uow:
        try:
            payload = jwt.decode(token, settings.S3_SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError as e :
            logging.error(e)
            raise credentials_exception
        user = await uow.users.get(name=username)
        if user is None:
            raise credentials_exception
        return user


CURUser = Annotated[UserDB, Depends(get_current_user)]

async def get_verificated_user(current_user: CURUser):
    if not current_user.verificated:
        raise HTTPException(status_code=400, detail="Non verificated user")
    return current_user

VERUser = Annotated[UserDB, Depends(get_verificated_user)]