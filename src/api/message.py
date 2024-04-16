from fastapi import APIRouter, Depends

from api.dependencies import UOWDep, get_redis
from services.message_service import MessageService
from schemas import CreateMessage, MessageDB
from utils.unit_of_work import IUnitOfWork, UnitOfWork

router = APIRouter(
    prefix="/messages"

)



@router.post("/create")
async def create_message( mes: CreateMessage, uow: UOWDep, redis=Depends(get_redis)):
   res = await  MessageService().create(uow=uow, new_message= mes)
   return res
    

@router.get('/get/{hash_value}')
async def get_message(uow: UOWDep, hash_value:str, redis=Depends(get_redis)):
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