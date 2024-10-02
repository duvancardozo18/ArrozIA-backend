from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.landModel import Land
from src.schemas.landSchema import LandSchema, UpdateLandSchema


def createLand(land:  LandSchema, session: Session = Depends(get_session) ):
    
    newLand = Land(nombre = land.nombre, finca_id = land.finca_id, area = land.area, latitud = land.latitud, longitud = land.longitud)
    #newLand = Land(nombre = land.nombre, finca_id = land.finca_id, area = land.area, unidad_area_id = land.unidad_area_id, latitud = land.latitud, longitud = land.longitud)
    session.add(newLand)
    session.commit()
    session.refresh(newLand)
    
    return {"msg": "Lote creada satisfactoriamente"}

def getAllLands(session: Session = Depends(get_session)):
    lands = session.query(Land).all()
    return lands

def getLandById(land_id: int, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )
    return land

def updateLand(land_id: int, land_data: UpdateLandSchema, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )

    # Convertir land_data a un diccionario y excluir valores no enviados
    update_data = land_data.dict(exclude_unset=True)

    # Actualizar solo los campos que se han enviado
    for key, value in update_data.items():
        setattr(land, key, value)

    session.commit()
    session.refresh(land)

    return {"msg": "Lote actualizado satisfactoriamente"}

def deleteLand(land_id: int, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )

    session.delete(land)
    session.commit()

    return {"msg": "Lote eliminado satisfactoriamente"}