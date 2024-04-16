import logging

from fastapi import HTTPException
from schemas.user_schemas import UserCreateSchema
from services.auth_service import get_password_hash
from utils.unit_of_work import IUnitOfWork


class UserService():

    async def create(self, uow: IUnitOfWork, new_user: UserCreateSchema):
        async with uow:
            try:

                password_hash = get_password_hash(new_user.password)
                setattr(new_user, "password_hash", password_hash)
                delattr(new_user, "password")
                
                user_id = await uow.users.create(new_user.model_dump())
                
                await uow.commit()
                return "OK"
                
            except Exception as e:
                await uow.rollback()
                logging.error(e)
                raise HTTPException(status_code=500)
        

    async def read(self, uow: IUnitOfWork, hash_value: str):
        async with uow:
            # try:
                # if await uow.redis.exists(hash_value):
                #     return await get_message_from_cache(hash_value)
                
                res  = await uow.messages.get(filters={"id_hash":hash_value})
                               
                mes = MessageDB.model_validate(res, from_attributes=True)
                # if user.folowert > 10000:
                # await save_message_to_cache(hash_value, mes)
                # uow.redis.set(key=hash_value, value=mes, expire=3600)
                return mes

            # except Exception as e:
                logging.error(e)
                await uow.rollback()
                raise HTTPException(status_code=500)
        

    async def update(self, uow: IUnitOfWork, hash_value: str, updates: MessageUpdate):
        async with uow:
            try:
                
                # message_db = await self.read(uow, hash_value)
                # await uow.redis.set(hash_value, )

                mes_db = await uow.messages.update(filters={"id_hash": hash_value}, 
                                            data={
                                                "name": updates.name,    
                                                "message_url": mes_url                              
                                            })
                mes = MessageDB().model_validate(mes_db, from_attributes=True)
                # if await uow.redis.exists(hash_value)
                mes_url = S3service.save_message(hash_value, updates.body)
                
                
                await uow.commit()
                return settings.APP_URL + f"/message//get_message/{hash_value}"
                
            
            except Exception as e:
                logging.error(e)
                await uow.rollback()


    async def delete(self, uow: IUnitOfWork, hash_value: str):
        async with uow:
            try:
                await uow.messages.delete(filters={"hash_value":hash_value})
                S3service.delete_message(hash_value)
                # await uow.redis.delete(hash_value)

                await uow.commit()
                return "Message was deleted"
                
            except Exception as e:
                logging.error(e)
                await uow.rollback()


    