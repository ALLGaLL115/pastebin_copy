from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schemas import UserCreateSchema
from services.auth_service import AuthenticationService
from api.dependencies import UOWDep
from services.user_service import UserService


router = APIRouter()


@router.post("/sing_up")
async def registrate_user(uow: UOWDep, new_user: UserCreateSchema):
    res = await UserService().create(uow, new_user)

@router.post("/login")
async def create_acces_token(uow: UOWDep, form_data: OAuth2PasswordRequestForm):
    res = await AuthenticationService().login(uow, form_data)
    return res

