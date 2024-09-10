from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.landController import (createLand, deleteLand, getAllLands,
                                           getLandById, updateLand)
from src.database.database import get_session
from src.schemas.landSchema import LandSchema

LAND_ROUTES = APIRouter()

@LAND_ROUTES.post('/register-land')
def register(land: LandSchema, session: Session = Depends(get_session)):
    return createLand(land, session)
    
@LAND_ROUTES.get('/lands', response_model=list[LandSchema])
def listLands(session: Session = Depends(get_session)):
    return getAllLands(session)

@LAND_ROUTES.get('/land/{land_id}', response_model=LandSchema)
def getLote(land_id: int, session: Session = Depends(get_session)):
    return getLandById(land_id, session)

@LAND_ROUTES.put('/update/land/{land_id}')
def updLand(land_id: int, land: LandSchema, session: Session = Depends(get_session)):
    return updateLand(land_id, land, session)

@LAND_ROUTES.delete('/delete/land/{land_id}')
def removeLand(land_id: int, session: Session = Depends(get_session)):
    return deleteLand(land_id, session)