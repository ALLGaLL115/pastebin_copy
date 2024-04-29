import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import ChunkedIteratorResult, select
from models import User
from services.verification_service import VerificationCodeCreate, VerificationCodeService
from shcemas.user_schemas import UserCreateSchema, UserDB
from services.auth_service import AuthenticationService, Tokenn, get_password_hash
from api.dependencies import CURUser, UOWDep, get_current_user
from services.user_service import UserService
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, NoResultFound

from tasks.verification_task import send_email_code


from sqlalchemy.exc import IntegrityError
from email_validator import EmailSyntaxError, validate_email


router = APIRouter(
    tags=['Auth']
)


@router.post("/sing_up")
async def registate_user(uow: UOWDep, new_user: UserCreateSchema):
# Перенести всё в сервис 
 async with uow:
        try:
            validate_email(new_user.email)

            chk = await uow.users.check_unique_values(email=new_user.email, name=new_user.name)
            data_dict = {"name":new_user.name, "email":new_user.email, "password_hash": get_password_hash(new_user.password)}
            if chk == "update":
                user: UserDB = await uow.users.update(data=data_dict, email=new_user.email)
            if chk == "create":
                user: UserDB = await uow.users.create(**data_dict)
            code =  await VerificationCodeService().create(uow, user_id=user.id)
            if code is None:
                    return JSONResponse(content ={"message":"succes", "user_id": user.id}, status_code=200)
            else:
                send_email_code.delay(email=new_user.email, code = code)
                await uow.commit()
                return JSONResponse(content ={"message":"succes", "user_id": user.id}, status_code=200)


        except EmailSyntaxError as e:
            raise HTTPException(status_code=400, detail={"error":e.__str__()})

        except HTTPException:
            raise

        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=500)     
        

# Есть ли такой код 
# код 200 : Узнать по какой причине(условиям) его нет
# по user_id, по коду и время
# если таких нет создать новый 

@router.post("/verification")
async def verificate(uow: UOWDep, code: str, user_id: int):
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

@router.post("/recreate_code")
async def recreate_code(uow: UOWDep, user_id: int):
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

        except HTTPException:
            raise 

        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=500) 


        

@router.post("/login")
async def login(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    res = await AuthenticationService.login(uow=uow, form_data=form_data)
    return res 


