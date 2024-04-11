import logging

from fastapi import HTTPException
from shemas import CreateMessage, MessageRead, MessageUpdate
from utils.unit_of_work import IUnitOfWork
import hashlib
from object_storage import delete_message, save_message
from config import settings




class MessageService:
    async def create(self, uow: IUnitOfWork, new_message: CreateMessage):
        try:
            mess_id = await uow.messages.create(data=new_message.model_dump())

            hash_value = hashlib.sha256(str(mess_id).encode())

            url = save_message(hash_value=hash_value, body=new_message.body)

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
        try:
            res  = await uow.messages.get(filters={"id_hash":hash_value})
            mes = MessageRead().model_validate(res, from_attributes=True)
            return mes

        except Exception as e:
            logging.error(e)
            await uow.rollback()

    async def update(self, uow: IUnitOfWork, hash_value: str, updates: MessageUpdate):
        try:
            message_db = await self.read(uow, hash_value)

            mes_url = save_message(hash_value, updates.body)

            await uow.messages.update(filters={"id_hash": hash_value}, 
                                        data={
                                            "name": updates.name,    
                                            "message_url": mes_url                              
                                        })
            await uow.commit()
            return settings.APP_URL + f"/message//get_message/{hash_value}"
            
        
        except Exception as e:
            logging.error(e)
            await uow.rollback()

    async def delete(self, uow: IUnitOfWork, hash_value: str):
        try:
            delete_message(hash_value)
            await uow.messages.delete(filters={"hash_value":hash_value})
            await uow.commit()
            return "Message was deleted"
            
        except Exception as e:
            logging.error(e)
            await uow.rollback()


    
        


        

        
