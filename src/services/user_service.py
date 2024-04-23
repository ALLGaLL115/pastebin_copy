import logging

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from shcemas.user_schemas import UserCreateSchema, UserDBSchema, UserReadSchema
from services.auth_service import get_password_hash
from utils.unit_of_work import IUnitOfWork, UnitOfWork

from email_validator import EmailNotValidError, validate_email

from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class UserService():

    async def create(self, uow: IUnitOfWork, new_user: UserCreateSchema):
        async with uow:
            
            try:
                validate_email(new_user.email)
                password_hash = get_password_hash(new_user.password)
                data = new_user.model_dump()
                del data['password']
                data['hashed_password'] = password_hash
                
                
                user_id = await uow.users.create(data=data)
                

            except IntegrityError as e:
                # await uow.rollback() 
                if "users_email_key" in str(e):
                    await uow.rollback()
                    res = await uow.users.check_verification(filters={"email": new_user.email})
                    if res:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already used")
                    del data["email"]
                    user_id = await uow.users.update(filters={"email":new_user.email}, data=data)
                    await uow.commit()
                    return user_id     
                    
                        
                if "users_name_key" in str(e):
                    await uow.rollback()
                    res = await uow.users.check_verification(filters={"name": new_user.name})
                    if res:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This username is already used")
                    else: 
                        del data["name"]
                        new_user_id = await uow.users.update(filters={"name": new_user.name}, data=data)
                        await uow.commit()
                        return new_user_id 
                        # await uow.verification_codes.create(data={"user_id":user_id, "email":new_user.email})

            except EmailNotValidError as e:
                logging.error(e)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This email is not exists')


            # except Exception as e:
            #     await uow.rollback()
            #     logging.error(e)
            #     raise HTTPException(status_code=500)
        

    async def update(self, uow: IUnitOfWork, curent_user: UserDBSchema, email: str, updates: UserCreateSchema):
        async with uow:
            try:
                user_new = await uow.users.update(filters={"id":curent_user.id})

                return UserReadSchema.model_validate(user_new, from_attributes=True)

                
                
            except IntegrityError as e:
                await uow.rollback() 
                if "users_email_key" in str(e):
                    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already used")
                if "users_name_key" in str(e):
                    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This username is already used")
                
            except Exception as e:
                logging.error(e)
                await uow.rollback()


    async def delete(self, uow: IUnitOfWork, curent_user: UserDBSchema):
        async with uow:
            try:
                user_id_deleted = await uow.users.delete(filters={"id":curent_user.id})

                await uow.commit()
                return JSONResponse(content=f"User with {user_id_deleted} was delete", status_code=200)
                
            except Exception as e:
                logging.error(e)
                await uow.rollback()


    