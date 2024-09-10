from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.farmCrontroller import (createFarm, deleteFarm,
                                            getAllFarms, getFarmById,
                                            updateFarm)
from src.database.database import get_session
from src.schemas.farmSchema import FarmSchema

FARM_ROUTES = APIRouter()

@FARM_ROUTES.post('/register-farm')
def register(farm: FarmSchema, session: Session = Depends(get_session)):
    return createFarm(farm, session)
    
@FARM_ROUTES.get('/farms', response_model=list[FarmSchema])
def allFarms(session: Session = Depends(get_session)):
    return getAllFarms(session)

@FARM_ROUTES.get('/farm/{farm_id}', response_model=FarmSchema)
def gotFarm(farm_id: int, session: Session = Depends(get_session)):
    return getFarmById(farm_id, session)

@FARM_ROUTES.put('/update/farm/{farm_id}')
def updaFarm(farm_id: int, farm: FarmSchema, session: Session = Depends(get_session)):
    return updateFarm(farm_id, farm, session)

@FARM_ROUTES.delete('/delete/farm/{farm_id}')
def removeFarm(farm_id: int, session: Session = Depends(get_session)):
    return deleteFarm(farm_id, session)