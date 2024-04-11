from fastapi import FastAPI, Query, HTTPException
from object_storage import upload_file_to_yandex
from database import asycn_session_maker
from shemas import CreateMessage, MessageDB, MessageRead

import aioredis
from contextlib import asynccontextmanager

redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    redis = await aioredis.create_redis(address=(redis, 6379))
    yield
    await redis.wait_closed()

app = FastAPI(lifespan=lifespan)




@app.post("/create_message")
async def create_message(mes: CreateMessage):


    pass

@app.get('/get_message/{hash_value}')
async def get_message(hash_value: str):
   
   cache = await redis.get(hash_value)
   pass


        






    

   
       

   
   

# @app.get("/messages")
# async def get_message(mes_hash: str):
#     mes = await mes_service.get_mes(mes_hash)
#     mes_body = await s3.get(url = mes.hash)
#     return {mes_metadata: mes.metadata, body: mes_body}
    
