from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.fincaCrontroller import (createFinca, deleteFinca,
                                             getAllFincas, getFincaById,
                                             updateFinca)
from src.database.database import get_session
from src.schemas.fincaSchema import FincaSchema

FINCA_ROUTES = APIRouter()

@FINCA_ROUTES.post('/registrar-finca')
def register(finca: FincaSchema, session: Session = Depends(get_session)):
    return createFinca(finca, session)
    
@FINCA_ROUTES.get('/fincas', response_model=list[FincaSchema])
def todasFincas(session: Session = Depends(get_session)):
    return getAllFincas(session)

@FINCA_ROUTES.get('/finca/{finca_id}', response_model=FincaSchema)
def obtenerFinca(finca_id: int, session: Session = Depends(get_session)):
    return getFincaById(finca_id, session)

@FINCA_ROUTES.put('/actualizar/finca/{finca_id}')
def actualizarFinca(finca_id: int, finca: FincaSchema, session: Session = Depends(get_session)):
    return updateFinca(finca_id, finca, session)

@FINCA_ROUTES.delete('/delete/finca/{finca_id}')
def eliminarFinca(finca_id: int, session: Session = Depends(get_session)):
    return deleteFinca(finca_id, session)