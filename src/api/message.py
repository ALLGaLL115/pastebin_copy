from fastapi import APIRouter, Depends
from redis import Redis

from api.dependencies import CURUser, UOWDep, VERUser, get_redis
from services.message_service import MessageService
from schemas import CreateMessage, MessageDB
from utils.unit_of_work import IUnitOfWork, UnitOfWork

from models import Message

router = APIRouter(
   tags=["Message"],
   prefix="/messages"

)

# проверка кода :
# Код в бд и время еще ест:
# Обновить пользоваетля: создать и отправить новый код по email



# Только верифицированный пользователь может 
# создавать обновлять и удалять комментарии,
# при этом только свои. добавить проверки на 
# то верифицирован ли пользователь, его ли это посты

# Не верифицированный пользоваетль может получать данные

# Условия для сохранения в кеш:
#    много подписчиков(Добавить в бд)
#    популярный пост

# Добавить проверку на наличие в кеше
# вынести в отдельную функцию

# Добавить укороченные хеши для ссылки на метаданные 

# Как работать с хешем для s3 

# Написать сервис генерирующий хеши заранее
# которые будут храниться в кеше 
#    Избежать колизии

# Отдельный сервис для редис 
# время зранения в кеше час(просто чтоб не засорять )




# Тесты:
# Тесты на авторизацию 
# Тесты на посты 
# Тесты для redis 
# тесты для Celery


@router.post("/create")
async def create_message( name: str, body: str, uow: UOWDep, user: VERUser, redis: Redis=Depends(get_redis)):
   async with uow:
      
      res = await  MessageService().create(uow=uow, user=user, new_message= CreateMessage(name=name, body=body, user_id=user.id), redis=redis)
      return res
      

@router.get('/get/{hash_value}')
async def get_message(uow: UOWDep, hash_value:str, user: VERUser, redis=Depends(get_redis)):
   if await redis.exists(hash_value) == 0:
      res = await MessageService().read(uow, hash_value)
      await redis.set(hash_value, res.model_dump_json())
      return res

   res = await redis.get(hash_value)
   return  MessageDB.model_validate_json(res)
   

@router.put("/update")
async def update_message(uow: UOWDep, hash_value: str, mes: CreateMessage):
   res = await MessageService().update(uow, hash_value, mes)
   return res


@router.delete("/delete")
async def delete_message(uow: UOWDep, hash_value:str):
   res = await MessageService().delete(uow, hash_value)
   return res