from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.farmModel import Farm
from src.schemas.farmSchema import FarmSchema, UpdateFarmSchema


def createFarm(farm:  FarmSchema, session: Session = Depends(get_session) ):
    
    newFarm = Farm(nombre = farm.nombre, ubicacion = farm.ubicacion, area_total = farm.area_total, latitud= farm.latitud, longitud = farm.longitud)
    session.add(newFarm)
    session.commit()
    session.refresh(newFarm)
    
    return {"msg": "finca creada satisfactoriamente"}


def getAllFarms(session: Session = Depends(get_session)):
    farms = session.query(Farm).all()
    return farms

def getFarmById(farm_id: int, session: Session = Depends(get_session)):
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )
    return farm

def updateFarm(farm_id: int, farm_data: UpdateFarmSchema, session: Session = Depends(get_session)):
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )

    farm.nombre = farm_data.nombre
    farm.ubicacion = farm_data.ubicacion
    farm.area_total = farm_data.area_total
    farm.latitud = farm_data.latitud
    farm.longitud = farm_data.longitud

    session.commit()
    session.refresh(farm)

    return {"msg": "Finca actualizada satisfactoriamente"}

def deleteFarm(farm_id: int, session: Session = Depends(get_session)):
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )

    session.delete(farm)
    session.commit()

    return {"msg": "Finca eliminada satisfactoriamente"}

