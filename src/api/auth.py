import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import ChunkedIteratorResult, select
from models import User
from services.verification_service import VerificationCodeCreate, VerificationCodeService
from shcemas.user_schemas import UserCreateSchema, UserDBSchema
from services.auth_service import AuthenticationService, Tokenn, get_password_hash
from api.dependencies import CURUser, UOWDep, get_current_user
from services.user_service import UserService
from pydantic import BaseModel

from tasks.verification_task import send_email_code


from sqlalchemy.exc import IntegrityError
from email_validator import EmailSyntaxError, validate_email


router = APIRouter()






@router.post('/sing_up')
async def registrate_user(uow: UOWDep, new_user: UserCreateSchema):
    async with uow:
        try:
            validate_email(new_user.email)

            query = select(User).filter_by(email=new_user.email, name=new_user.name)
            users_db = await uow.session.execute(query)
            users_db = users_db.scalars().all()
            
            if len(users_db) == 0:
                user = User(name=new_user.name, email=new_user.email, password_hash=get_password_hash(new_user.password))
                uow.session.add(user)
                await uow.commit()
                print(user.id)
                code =  await VerificationCodeService().create(uow, VerificationCodeCreate(user_id=user.id, email=user.email))
                send_email_code.delay(email=new_user.email, code = code)

                return JSONResponse(content ={"message":"succes", "user_id": user.id}, status_code=200)
            else:
                erors = []
                print(users_db)
                for i in users_db:
                    if new_user.email == i.email:
                        erors.append("This email is already used")
                    if new_user.name == i.name:
                        erors.append("This username is already used")
                
                raise HTTPException(status_code=409, detail= {"errors": erors})
                


        except EmailSyntaxError as e:
            raise HTTPException(status_code=400, detail={"error":e.__str__()})

        except IntegrityError as e:
            if "users_email_key" in e._message():
                raise HTTPException(status_code=409, detail= "This email is already used")
            if "users_name_key" in e._message():
                raise HTTPException(status_code=409, detail= "This username is already used")
        # except Exception as e:
        #     logging.error(e)
        #     if e == HTTPException:
        #         raise
        #     raise HTTPException(status_code=500)        



@router.post("/verification")
async def verificate(uow: UOWDep, code: str, user_id: int):
    async with uow:
        user = await uow.session.get(User, user_id)
        res = await VerificationCodeService().validate(uow, user.id, code)     
        return res
        

@router.post("/login")
async def login(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    res = await AuthenticationService.login(uow=uow, form_data=form_data)
    return res 



        
        


# @router.post("/sing_up")
# async def registrate_user(uow: UOWDep, new_user: UserCreateSchema):
#         # try:
#             user_id = await UserService().create(uow, new_user)
#             code = await VerificationCodeService().create(
#                 uow, code_create_model=VerificationCodeCreate(
#                     user_id=user_id, email=new_user.email
#                     ))
#             send_email_code.delay(email=new_user.email, code = code)

#             return JSONResponse("success", 200)
#         # except Exception as e:
#         #     logging.error(e)
#         #     raise HTTPException(status_code=500)
        

        
        


# @router.post("/verify_by_email")
# async def verificate_user(uow: UOWDep, email: str, code: str, ):
#     res = await VerificationCodeService().validate(uow,  code)
#     return res




# @router.post("/login")
# async def create_acces_token(form_data:  Annotated[OAuth2PasswordRequestForm, Depends()], uow: UOWDep):
#     res = await AuthenticationService.login(uow, form_data)
#     return res




