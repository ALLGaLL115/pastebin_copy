import logging
from random import randint

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from schemas.message_schemas import CreateMessage, MessageDB, MessageUpdate
from schemas.user_schemas import UserDB
from utils.unit_of_work import IUnitOfWork
import hashlib
from config import settings
from repositories.s3_repository import S3Repository

from sqlalchemy.exc import NoResultFound



# https://host/messages/message_hash - по этой ссылке будут получаться метаданные и в них будет url ниже который будет вести либд в s3 либо в redis хранилище
# https://host/messages/data/data_hash это будет передаваться в xml



class MessageService:
    async def create(self, uow: IUnitOfWork, user:UserDB, new_message: CreateMessage, redis: Redis):
        async with uow:
            try:
                hash_value = hashlib.sha256(str(randint(1000000, 9999999)).encode()).hexdigest()
                url = S3Repository().save_message(hash_value=hash_value, body=new_message.body)
                mess: MessageDB = await uow.messages.create(name=new_message.name, user_id=user.id, hash_id=hash_value, message_url=url)
                folowers_count = await uow.subscriptions.get_count(target_id=user.id)
                print(folowers_count)
                if folowers_count >= 3:
                    await redis.set(hash_value+"data", new_message.body, nx=True, ex= 3600)
                    mess.message_url = f"https://{settings.APP_HOST}/messages/data/{hash_value}"
                    print(mess.message_url)
                    await redis.set(hash_value+"metadata", mess.model_dump_json(),nx=True, ex= 3600)
                    

                await uow.commit()

                return settings.APP_HOST + f"/messagess/{hash_value}"
            except Exception as e:
                logging.error(e)
                await uow.rollback()
                raise 
        

    async def read(self, uow: IUnitOfWork, hash_value: str, redis: Redis):
        try:
        
            re = await redis.get(hash_value)
            if re:
                return MessageDB.model_validate(re)
            async with uow:
                    res  = await uow.messages.get(hash_id=hash_value)
                    return res            
        except HTTPException as e:
            raise
        
        except Exception as e:
            logging.exception(e)
            raise

    async def update(self, uow: IUnitOfWork, hash_value: str, updates: MessageUpdate, ver_user: UserDB, redis: Redis):
        try:
            data = []
            if updates.body:
                print(1)
                mes_url = S3Repository().save_message(hash_value, updates.body)
                data["message_url"] = mes_url
            if updates.name:
                data["name"] = updates.name
            
            if len(data) > 0:

                mes_db = await uow.messages.update(
                                            data={
                                                "name": updates.name,    
                                                "message_url": mes_url                              
                                            },
                                            hash_id=hash_value
                                            )
                

                re = await redis.get(hash_value)
                if re:
                    await redis.set(hash_value, mes_db.model_dump_json(), xx=True, keepttl=True)
                    
                
                await uow.commit()
                return JSONResponse(content={"status":"success"}, status_code=200)
            else: 
                return JSONResponse(content={"detail":"You dont add any update"}, status_code=400)
            
        
        except Exception as e:
            logging.exception(e)
            await uow.rollback()
            raise

    async def delete(self, uow: IUnitOfWork, hash_value: str, ver_user: UserDB, redis: Redis):
        re = await redis.get(hash_value)
        if re:
            await redis.delete(hash_value)
        try:
            await uow.messages.delete(hash_id=hash_value)
            S3Repository().delete_message(hash_value)
            # await uow.redis.delete(hash_value)

            await uow.commit()
            return JSONResponse(content={"status":"success"}, status_code=200)
            NoResultFound

        except NoResultFound as e:
            raise HTTPException(status_code=404, detail="This message is not exsists")
        except Exception as e:
            logging.exception(e)
            await uow.rollback()
            raise



    
        


        

        
