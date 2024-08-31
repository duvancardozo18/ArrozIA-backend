from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.loteModel import Lote
from src.schemas.loteSchema import LoteSchema


def createLote(lote:  LoteSchema, session: Session = Depends(get_session) ):
    
    newLote = Lote(nombre = lote.nombre, finca_id = lote.finca_id, area = lote.area, unidad_area_id = lote.unidad_area_id, latitud = lote.latitud, longitud = lote.longitud)
    session.add(newLote)
    session.commit()
    session.refresh(newLote)
    
    return {"msg": "Lote creada satisfactoriamente"}

def getAllLotes(session: Session = Depends(get_session)):
    lotes = session.query(Lote).all()
    return lotes

def getLoteById(lote_id: int, session: Session = Depends(get_session)):
    lote = session.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {lote_id} no encontrado"
        )
    return lote

def updateLote(lote_id: int, lote_data: LoteSchema, session: Session = Depends(get_session)):
    lote = session.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {lote_id} no encontrado"
        )

    lote.nombre = lote_data.nombre
    lote.finca_id = lote_data.finca_id
    lote.area = lote_data.area
    lote.unidad_area_id = lote_data.unidad_area_id
    lote.latitud = lote_data.latitud
    lote.longitud = lote_data.longitud

    session.commit()
    session.refresh(lote)

    return {"msg": "Lote actualizado satisfactoriamente"}

def deleteLote(lote_id: int, session: Session = Depends(get_session)):
    lote = session.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {lote_id} no encontrado"
        )

    session.delete(lote)
    session.commit()

    return {"msg": "Lote eliminado satisfactoriamente"}