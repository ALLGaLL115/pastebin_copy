
import datetime
from email.mime.text import MIMEText
import logging
import secrets
import string

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
import smtplib
from email.message import EmailMessage

from models import VerifycationCode
from utils.unit_of_work import IUnitOfWork
from config import settings


class VerificationCodeCreate(BaseModel):
    user_id: int
    email: str

def generate_verification_code(length = 6):
    alphabet = string.digits
    verifycation_code = ''.join(secrets.choice(alphabet) for _ in range(length))

    return verifycation_code


class VerificationCodeService:

    async def create(self, uow: IUnitOfWork, user_id:int)-> str|None:  
        # async with uow:
            while True:
                try:
                    existing_code: VerifycationCode = await uow.verification_codes.get_valid_user_code(user_id=user_id)
                    # print(existing_code)
                    if existing_code == None:
                        verification_code = generate_verification_code()                            
                        await uow.verification_codes.create(user_id=user_id, code= verification_code, expiry_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1))
                        # await uow.commit()
                        return verification_code   
                    else:
                        return None
                except IntegrityError as e:                
                    if "users_code_key" in str(e):
                        # await uow.rollback()
                        continue

                    
                
               
    async def validate_code(self, uow:IUnitOfWork, user_id: int, code:str):
        async with uow:
            try:
                await uow.verification_codes.validate_code(code=code, user_id=user_id)
                await uow.users.update(data={"verificated":True}, id=user_id)
                await uow.commit()
                return JSONResponse(content="Succes", status_code=200)
            
            except NoResultFound as e:
                logging.error(e)
                await uow.rollback()
                uow.verification_codes.create()
                raise HTTPException(status_code=404, detail="Wrong code")
            
            # except Exception as e:
            #     logging.error(e)
            #     await uow.rollback()
            #     raise HTTPException(status_code=500)

            



                        
   