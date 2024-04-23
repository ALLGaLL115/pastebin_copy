
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

    async def create(self, uow: IUnitOfWork, code_create_model: VerificationCodeCreate):  
        async with uow:
            while True:
                try:
                    verification_code = generate_verification_code()
                    await uow.verification_codes.create(data={"user_id": code_create_model.user_id, "code": verification_code})
                    break
                except IntegrityError as e:                
                    if "users_code_key" in str(e):
                        await uow.rollback()
                        continue

            await uow.commit()
            return verification_code
                
               
    async def validate(self, uow:IUnitOfWork, user_id: int, code:str):
        async with uow:
            try:
                await uow.verification_codes.verificate(code=code)
                await uow.users.update(filters={"id":user_id}, data={"role":2})
                await uow.commit()
                return JSONResponse(content="Succes", status_code=200)
            
            except NoResultFound as e:
                logging.error(e)
                await uow.rollback()
                # raise HTTPException(status_code=404, detail="Wrong code")
            
            except Exception as e:
                logging.error(e)
                await uow.rollback()
                raise HTTPException(status_code=500)

            



                        
   