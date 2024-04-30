from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from api.dependencies import CURUser, UOWDep
from models import Subscription


router = APIRouter(
    tags=["subcriptions"],
    prefix="/subs"
)


@router.post("/subscribe")
async def subscribe(uow:UOWDep, cur_user: CURUser, target_id: int):
    async with uow:
        await uow.subscriptions.create(
            subscriber_id = cur_user.id, target_id = target_id
        )
        return JSONResponse(status_code=200, content={"detail":"success"})
    

@router.post("/unsubcribe")
async def unsubscribe(uow:UOWDep, cur_user: CURUser, target_id: int):
    async with uow:
        await uow.subscriptions.delete(
            subscriber_id = cur_user.id, target_id = target_id
        )
        return JSONResponse(status_code=200, content={"detail":"success"})
    