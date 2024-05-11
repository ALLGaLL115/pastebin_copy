
from datetime import timedelta, timezone, datetime
import logging
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import VerifycationCode
from schemas.auth import Tokenn
from schemas.user_schemas import UserCreateSchema, UserDB
from services.verification_service import VerificationCodeService
from tasks.verification_task import send_email_code
from utils.unit_of_work import IUnitOfWork, UnitOfWork
from email_validator import EmailSyntaxError, EmailUndeliverableError, validate_email
from config import settings
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.exc import IntegrityError, NoResultFound


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password):
    return pwd_context.hash(password)




async def authenticate_user(uow: IUnitOfWork, username: str, password: str):
        user: UserDB = await uow.users.get(name=username)
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user
    

def create_access_token(data: dict, live_time_minutes: int|None= None):
    expires_delta = timedelta(minutes=live_time_minutes)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.S3_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt



class AuthenticationService:


    async def registration(uow:UnitOfWork, new_user:UserCreateSchema):
        async with uow:
            try:
                validate_email(new_user.email)

                chk = await uow.users.check_unique_values(email=new_user.email, name=new_user.name)
                data_dict = {"name":new_user.name, "email":new_user.email, "password_hash": get_password_hash(new_user.password)}
                if chk == "update":
                    user: UserDB = await uow.users.update(data=data_dict, email=new_user.email)
                if chk == "create":
                    user: UserDB = await uow.users.create(**data_dict)
                await uow.commit()
                return JSONResponse(content ={"status":"succes", "user_id": user.id}, status_code=200)


            except EmailSyntaxError as e:
                await uow.rollback()
                raise HTTPException(status_code=400, detail={"error":e.__str__()})
            
            except EmailUndeliverableError as e:
                await uow.rollback()
                raise HTTPException(status_code=400, detail={"error":e.__str__()})

            except HTTPException:
                await uow.rollback()
                raise
        
            except Exception as e:
                logging.error(e)
                await uow.rollback()
                raise HTTPException(status_code=500, detail=f"{e}")     
            
    
    async def send_code(uow: UnitOfWork, user_id: int):
        async with uow:
            try:
                user:UserDB = await uow.users.get(id=user_id)
                code= await VerificationCodeService().create(uow, user_id)
                if code is None:
                    return JSONResponse(content ={"message":"succes", "user_id": user_id}, status_code=200)
                else:
                    send_email_code.delay(email=user.email, code = code)
                    await uow.session.commit()
                    await uow.session.close()  
                    return JSONResponse(content ={"message":"succes", "user_id": user_id}, status_code=200)
            except EmailSyntaxError as e:
                    raise HTTPException(status_code=400, detail={"error":e.__str__()})

            except HTTPException as e:
                logging.exception(e)
                raise 

            # except Exception as e:
            #     logging.exception(e)
            #     raise HTTPException(status_code=500) 
            

    async def verification(uow: UnitOfWork, code: str, user_id: int):
        async with uow:
            try:

                await uow.verification_codes.validate_code(code=code, user_id=user_id)
                await uow.users.update(data={"verificated":True}, id=user_id)
                await uow.commit()
                return JSONResponse(content="Succes", status_code=200)
            
            except NoResultFound as e:
                logging.error(e)
                await uow.rollback()
                raise HTTPException(status_code=404, detail="Wrong code")


    async def login(uow: IUnitOfWork, form_data: OAuth2PasswordRequestForm) -> Tokenn:
        async with uow:
            user = await authenticate_user(uow, form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token = create_access_token(
                data={"sub": user.name}, live_time_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            return Tokenn(access_token=access_token, token_type="bearer")