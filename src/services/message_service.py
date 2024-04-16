import logging

from fastapi import HTTPException
from schemas import CreateMessage, MessageDB, MessageRead, MessageUpdate
from utils.unit_of_work import IUnitOfWork
import hashlib
from config import settings
from services.s3_service import S3service



class MessageService:
    async def create(self, uow: IUnitOfWork, new_message: CreateMessage):
        async with uow:
            try:
                mess_id = await uow.messages.create(data={"name": new_message.name})
                

                hash_value = hashlib.sha256(str(mess_id).encode()).hexdigest()

                url = S3service().save_message(hash_value=hash_value, body=new_message.body)
                print(url)

                await uow.messages.update(filters={"id":mess_id}, 
                                    data={
                                        "id_hash":hash_value,
                                        "message_url":url,
                                    })
                

                
                await uow.commit()
                return settings.APP_URL + f"/message/get_message/{hash_value}"
            except Exception as e:
                logging.error(e)
                await uow.rollback()
        

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
        try:
            await uow.messages.delete(filters={"hash_value":hash_value})
            S3service.delete_message(hash_value)
            # await uow.redis.delete(hash_value)

            await uow.commit()
            return "Message was deleted"
            
        except Exception as e:
            logging.error(e)
            await uow.rollback()


    
        


        

        
