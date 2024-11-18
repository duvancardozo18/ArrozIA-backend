from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.controller.preciosinsumoController import (
    get_inputs_by_crop,
    get_total_input_cost_by_crop,
    get_inputs_by_crop_and_partial_name
)
from src.schemas.preciosinsumoSchema import AgriculturalInputWithTipoSchema
from src.database.database import get_session

router = APIRouter()

#lista todos los insumos que se han usado en el cultivo
@router.get("/cultivos/{cultivo_id}/insumos", response_model=List[AgriculturalInputWithTipoSchema])
def list_inputs(cultivo_id: int, session: Session = Depends(get_session)):
    return get_inputs_by_crop(cultivo_id, session)

#dar el costo total de todos los insumos
@router.get("/cultivos/{cultivo_id}/insumos/total-cost", tags=["Insumos"])
def get_total_cost(cultivo_id: int, session: Session = Depends(get_session)):
    """
    Retorna el costo total de todos los insumos relacionados con un cultivo.
    """
    return get_total_input_cost_by_crop(cultivo_id, session)

#filtro para listar insumos, mediante nombres de insumos va filtrando
@router.get("/cultivos/{cultivo_id}/insumos/search", response_model=List[AgriculturalInputWithTipoSchema])
def search_inputs_by_partial_name(cultivo_id: int, concepto: str, session: Session = Depends(get_session)):
    return get_inputs_by_crop_and_partial_name(cultivo_id, concepto, session)
