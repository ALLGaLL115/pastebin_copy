from fastapi import APIRouter, Depends
from redis import Redis

from api.dependencies import CURUser, UOWDep, VERUser, get_redis
from schemas.message_schemas import CreateMessage, MessageUpdate
from services.message_service import MessageService
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
   # async with uow:
      
      res = await  MessageService().create(uow=uow, user=user, new_message= CreateMessage(name=name, body=body, user_id=user.id), redis=redis)
      return res
      

@router.get('/get/{hash_value}')
async def get_message(uow: UOWDep, hash_value:str, redis=Depends(get_redis)):
   res = await MessageService().read(uow, hash_value, redis)
   return  res
   

@router.put("/update")
async def update_message(uow: UOWDep, hash_value: str, ver_user: VERUser, updates: MessageUpdate, redis: Redis=Depends(get_redis)):  
   res = await MessageService().update(uow=uow, hash_value=hash_value, ver_user=ver_user, updates=updates, redis=redis)
   return res


@router.delete("/delete")
async def delete_message(uow: UOWDep, hash_value:str, ver_user:VERUser, redis: Redis=Depends(get_redis)):
   res = await MessageService().delete(uow=uow, hash_value=hash_value, ver_user=ver_user, redis=redis,)
   return res