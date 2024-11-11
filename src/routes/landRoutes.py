from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.landController import (createLand, deleteLand, getAllLands,
                                           getLandById, updateLand, calculate_total_rent, calculate_machinery_and_labor_costs, calculate_agricultural_input_costs)
from src.database.database import get_session
from src.schemas.landSchema import LandSchema, UpdateLandSchema

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
def updLand(land_id: int, land: UpdateLandSchema, session: Session = Depends(get_session)):
    return updateLand(land_id, land, session)

@LAND_ROUTES.delete('/delete/land/{land_id}')
def removeLand(land_id: int, session: Session = Depends(get_session)):
    return deleteLand(land_id, session)

# Nuevo endpoint para calcular el arriendo total
@LAND_ROUTES.get('/lands/{plot_id}/total-rent')
def get_total_rent(plot_id: int, session: Session = Depends(get_session)):
    return calculate_total_rent(plot_id, session)

#costos de maquinaria y mano de obra cultural
@LAND_ROUTES.get('/lands/{plot_id}/machinery-and-labor-costs')
def get_machinery_and_labor_costs(plot_id: int, session: Session = Depends(get_session)):
    return calculate_machinery_and_labor_costs(plot_id, session)

#Costos de insumos agricolas 
@LAND_ROUTES.get('/lands/{plot_id}/agricultural-input-costs')
def get_agricultural_input_costs(plot_id: int, session: Session = Depends(get_session)):
    return calculate_agricultural_input_costs(plot_id, session)
