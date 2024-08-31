from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.loteController import (createLote, deleteLote, getAllLotes,
                                           getLoteById, updateLote)
from src.database.database import get_session
from src.schemas.loteSchema import LoteSchema

LOTE_ROUTES = APIRouter()

@LOTE_ROUTES.post('/registrar-lote')
def register(lote: LoteSchema, session: Session = Depends(get_session)):
    return createLote(lote, session)
    
@LOTE_ROUTES.get('/lotes', response_model=list[LoteSchema])
def listLotes(session: Session = Depends(get_session)):
    return getAllLotes(session)

@LOTE_ROUTES.get('/lote/{lote_id}', response_model=LoteSchema)
def getLote(lote_id: int, session: Session = Depends(get_session)):
    return getLoteById(lote_id, session)

@LOTE_ROUTES.put('/actualizar/lote/{lote_id}')
def actualizarLote(lote_id: int, lote: LoteSchema, session: Session = Depends(get_session)):
    return updateLote(lote_id, lote, session)

@LOTE_ROUTES.delete('/eliminar/lote/{lote_id}')
def eliminarLote(lote_id: int, session: Session = Depends(get_session)):
    return deleteLote(lote_id, session)