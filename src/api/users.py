
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.dependencies import CURUser, UOWDep


router = APIRouter(
   tags=["User"],
   prefix="/users"

)


