from contextlib import asynccontextmanager
import logging
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from config import settings

from api.message import router as message_router
from api.auth import router as auth_router


REDIS_URL = 'redis://localhost'
REDIS_DB = 0
REDIS_PASS = 'RedisPassword'

redis = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis

    if redis is None:
        pool = aioredis.ConnectionPool.from_url(REDIS_URL)
        redis = await aioredis.Redis(connection_pool=pool)

    yield
    redis.close(close_connection_pool=True)


    

app = FastAPI(lifespan=lifespan)

@app.middleware(f"{settings.APP_HOST}/messages")
async def http_middleware(request: Request, call_next):
    global redis



    # Initial response when exception raised on 
    #  `call_next` function
    
    try:
        request.state.redis = redis
        response = await call_next(request)
        return response
    except Exception as e:
        logging.exception(e)

        # err = {'error': True, 'message': "Internal server error"},
        # response = JSONResponse(status_code=500)
        # return response
        raise
    # finally:
    #     response = JSONResponse(content="sdfs", status_code=500)
    #     return response
    

app.include_router(auth_router)
app.include_router(message_router)


        





    
