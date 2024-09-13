from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.farmRoleController import (getUserFarmRol,
                                               getUserFarmRolById)
from src.database.database import get_session
from src.schemas.farmRoleSchema import UserFarmRolSchema

USER_FARM_ROL_ROUTES = APIRouter()

@USER_FARM_ROL_ROUTES.get('/user-farm-rol', response_model=list[UserFarmRolSchema])
def userRol(session: Session = Depends(get_session)):
    return getUserFarmRol(session) 

@USER_FARM_ROL_ROUTES.get('/user-farm-rol/{user_id}', response_model=UserFarmRolSchema)
def userFarmRol(user_id: int, session: Session = Depends(get_session)):
    return getUserFarmRolById(user_id, session)
