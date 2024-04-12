from fastapi import APIRouter

from api.dependencies import UOWDep
from services.message_service import MessageService
from shemas import CreateMessage

router = APIRouter(
    prefix="/messages"

)



@router.post("/create")
async def create_message(uow: UOWDep, mes: CreateMessage):
   res = await  MessageService().create(uow=uow, new_message= mes)
   return res
    

@router.get('/get/{hash_value}')
async def get_message(uow: UOWDep, hash_value:str):
   res = await MessageService().read(uow, hash_value)
   return res

@router.put("/update")
async def update_message(uow: UOWDep, hash_value: str, mes: CreateMessage):
   res = await MessageService().update(uow, hash_value, mes)
   return res


@router.delete("/delete")
async def delete_message(uow: UOWDep, hash_value:str):
   res = await MessageService().delete(uow, hash_value)
   return res