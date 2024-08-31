from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.fincaModel import Finca
from src.schemas.fincaSchema import FincaSchema


def createFinca(finca:  FincaSchema, session: Session = Depends(get_session) ):
    
    newFinca = Finca(nombre = finca.nombre, ubicacion = finca.ubicacion, area_total = finca.area_total, latitud= finca.latitud, longitud = finca.longitud)
    session.add(newFinca)
    session.commit()
    session.refresh(newFinca)
    
    return {"msg": "finca creada satisfactoriamente"}


def getAllFincas(session: Session = Depends(get_session)):
    fincas = session.query(Finca).all()
    return fincas

def getFincaById(finca_id: int, session: Session = Depends(get_session)):
    finca = session.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {finca_id} no encontrada"
        )
    return finca

def updateFinca(finca_id: int, finca_data: FincaSchema, session: Session = Depends(get_session)):
    finca = session.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {finca_id} no encontrada"
        )

    finca.nombre = finca_data.nombre
    finca.ubicacion = finca_data.ubicacion
    finca.area_total = finca_data.area_total
    finca.latitud = finca_data.latitud
    finca.longitud = finca_data.longitud

    session.commit()
    session.refresh(finca)

    return {"msg": "Finca actualizada satisfactoriamente"}

def deleteFinca(finca_id: int, session: Session = Depends(get_session)):
    finca = session.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {finca_id} no encontrada"
        )

    session.delete(finca)
    session.commit()

    return {"msg": "Finca eliminada satisfactoriamente"}

