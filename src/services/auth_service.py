
from datetime import timedelta, timezone, datetime
import logging
from typing import Annotated
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from api.dependencies import UOWDep
from utils.unit_of_work import IUnitOfWork
from schemas.user_schemas import *

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "3FBAC6FC3B920B69A823BD2F41C86C6842E4A0AB88C00BD43BBCA5F19DE156FA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)




async def authenticate_user(uow: IUnitOfWork, username: str, password: str):
    async with uow:
        user: UserDBSchema = await uow.users().get(filters={"name": username})
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    

def create_access_token(data: dict, live_time_minutes: int|None= None):
    expires_delta = timedelta(minutes=expires_delta)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt










class SingUpForm(BaseModel):
    name: str
    email: str
    password: str







class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str|None = None



class AuthenticationService:
    # async def sing_in(self, uow: IUnitOfWork, data: SingUpForm):
    #     async with uow:
    #         try:
    #             user_id = await uow.users().create(data=data.model_dump())

    #         except Exception as e:
    #             logging.error(e)
    #             raise HTTPException(status_code=500)





    async def login(uow: IUnitOfWork, form_data: OAuth2PasswordRequestForm):
        user = await authenticate_user(uow, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user.username}, live_time_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return Token(access_token=access_token, token_type="bearer")















# async def get_current_active_user(
#     current_user: Annotated[UserReadSchema, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login_for_access_token(
#     uow: UOWDep,
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = authenticate_user(uow, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")


# @app.get("/users/me/", response_model=UserRead)
# async def read_users_me(
#     current_user: Annotated[UserRead, Depends(get_current_active_user)],
# ):
#     return current_user



