from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.unidadAreaController import getUnidadArea
from src.database.database import get_session
from src.schemas.unidadAreaSchema import UnidadAreaSchema

UNIDAD_AREA_ROUTE = APIRouter()

@UNIDAD_AREA_ROUTE.get('/unidades-areas', response_model=list[UnidadAreaSchema])
def unidadesAreas(session: Session = Depends(get_session)):
    return getUnidadArea(session)