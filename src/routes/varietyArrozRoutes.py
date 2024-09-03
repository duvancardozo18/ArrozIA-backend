from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.varietyArrozController import (
    createVariety, deleteVariety, getVariety, listVarieties, updateVariety
)
from src.database.database import get_session
from src.schemas.varietyArrozSchema import VariedadArrozCreate, VariedadArrozResponse

VARIETY_ARROZ_ROUTES = APIRouter()

@VARIETY_ARROZ_ROUTES.post('/registrar-variedad', response_model=VariedadArrozResponse)
def register_variety(variety: VariedadArrozCreate, session: Session = Depends(get_session)):
    return createVariety(variety, session)

@VARIETY_ARROZ_ROUTES.get('/variedades', response_model=list[VariedadArrozResponse])
def all_varieties(session: Session = Depends(get_session)):
    return listVarieties(session)

@VARIETY_ARROZ_ROUTES.get('/variedad/{variety_id}', response_model=VariedadArrozResponse)
def get_variety(variety_id: int, session: Session = Depends(get_session)):
    return getVariety(variety_id, session)

@VARIETY_ARROZ_ROUTES.put('/actualizar/variedad/{variety_id}', response_model=VariedadArrozResponse)
def update_variety(variety_id: int, variety: VariedadArrozCreate, session: Session = Depends(get_session)):
    return updateVariety(variety_id, variety, session)

@VARIETY_ARROZ_ROUTES.delete('/eliminar/variedad/{variety_id}')
def delete_variety(variety_id: int, session: Session = Depends(get_session)):
    return deleteVariety(variety_id, session)
