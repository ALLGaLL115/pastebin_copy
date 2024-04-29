import logging

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from shcemas.user_schemas import UserCreateSchema, UserDB, UserReadSchema
from services.auth_service import get_password_hash
from utils.unit_of_work import IUnitOfWork, UnitOfWork

from email_validator import EmailSyntaxError, validate_email

from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class UserService():

    # async def create(self, uow: IUnitOfWork, new_user: UserCreateSchema):
    #     async with uow:
    #         try:
    #             validate_email(new_user.email)

    #             chk = await uow.users.check_unique_values(email=new_user.email, name=new_user.name)
    #             data_dict = {"name":new_user.name, "email":new_user.email, "password_hash": get_password_hash(new_user.password)}
    #             if chk == "update":
    #                 user_id = await uow.users.update(data=data_dict, email=new_user.email)
    #             if chk == "create":
    #                 user_id = await uow.users.create(**data_dict)
    #             await uow.commit()
    #             return user_id
            
    #         except EmailSyntaxError as e:
    #             raise HTTPException(status_code=400, detail={"error":e.__str__()})

    #         except HTTPException:
    #             raise

            # except Exception as e:
            #     logging.error(e)
            #     raise HTTPException(status_code=500)     
        

    async def update(self, uow: IUnitOfWork, curent_user: UserDB, email: str, updates: UserCreateSchema):
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


    async def delete(self, uow: IUnitOfWork, curent_user: UserDB):
        async with uow:
            try:
                user_id_deleted = await uow.users.delete(filters={"id":curent_user.id})

                await uow.commit()
                return JSONResponse(content=f"User with {user_id_deleted} was delete", status_code=200)
                
            except Exception as e:
                logging.error(e)
                await uow.rollback()


    async def folow(self, uow: IUnitOfWork, curent_user: UserDB, target_id: int):
        async with uow:
            uow.subscriptions.create()



    