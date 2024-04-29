import logging

from fastapi import HTTPException
from redis import Redis
from schemas import CreateMessage, MessageDB, MessageRead, MessageUpdate
from shcemas.user_schemas import UserDB
from shcemas.utils import update_model
from utils.unit_of_work import IUnitOfWork
import hashlib
from config import settings
from repositories.s3_repository import S3Repository



class MessageService:
    async def create(self, uow: IUnitOfWork, user:UserDB, new_message: CreateMessage, redis: Redis):
        async with uow:
            try:
                mess: MessageDB = await uow.messages.create(data={"name": new_message.name})
                hash_value = hashlib.sha256(str(mess.id).encode()).hexdigest()
                url = S3Repository().save_message(hash_value=hash_value, body=new_message.body)
                await uow.messages.update(filters={"id":mess.id}, 
                                    data={
                                        "id_hash":hash_value,
                                        "message_url":url,
                                    })
                folowers_count = await uow.subscriptions.get_count(target_id=user.id)
                if folowers_count > 100000:
                    await redis.set(hash_value, mess.model_dump(),nx=True, ex= 3600)

                await uow.commit()

                return settings.APP_URL + f"/message/get_message/{hash_value}"
            except Exception as e:
                logging.error(e)
                await uow.rollback()
        

    async def read(self, uow: IUnitOfWork, user: UserDB, hash_value: str, redis: Redis):
       
        re = await redis.get(hash_value)
        if re:
            return MessageDB.model_validate(re)
        async with uow:
            # try:
                res  = await uow.messages.get(filters={"id_hash":hash_value})
                return res

            # except Exception as e:
                logging.error(e)
                await uow.rollback()
                raise HTTPException(status_code=500)

    async def update(self, uow: IUnitOfWork, hash_value: str, updates: MessageUpdate, redis: Redis):
        
        try:
            mes_db = await uow.messages.update(
                                        data={
                                            "name": updates.name,    
                                            "message_url": mes_url                              
                                        },
                                        id_hash=hash_value
                                        )
            mes = MessageDB().model_validate(mes_db, from_attributes=True)
            mes_url = S3service.save_message(hash_value, updates.body)

            re = await redis.get(hash_value)
            if re:
                new = update_model(MessageDB.model_validate(re),updates )
                await redis.set(hash_value, new.model_dump(), xx=True, keepttl=True)
                
            
            await uow.commit()
            return settings.APP_URL + f"/message//get_message/{hash_value}"
            
        
        except Exception as e:
            logging.error(e)
            await uow.rollback()

    async def delete(self, uow: IUnitOfWork, hash_value: str):
        try:
            await uow.messages.delete(filters={"hash_value":hash_value})
            S3service.delete_message(hash_value)
            # await uow.redis.delete(hash_value)

            await uow.commit()
            return "Message was deleted"
            
        except Exception as e:
            logging.error(e)
            await uow.rollback()


    
        


        

        
