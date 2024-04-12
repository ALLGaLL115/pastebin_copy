from fastapi import Depends
from typing import Annotated
from utils.unit_of_work import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]