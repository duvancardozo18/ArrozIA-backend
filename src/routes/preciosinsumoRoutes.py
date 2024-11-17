from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.preciosinsumoController import get_inputs_by_crop
from src.database.database import get_session
from src.schemas.preciosinsumoSchema import AgriculturalInputWithTipoSchema

router = APIRouter()

@router.get("/cultivos/{cultivo_id}/insumos", response_model=list[AgriculturalInputWithTipoSchema])
def read_inputs_by_crop(cultivo_id: int, session: Session = Depends(get_session)):
    """
    Obtiene todos los insumos relacionados con las tareas de un cultivo específico.
    """
    return get_inputs_by_crop(cultivo_id, session)
