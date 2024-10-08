from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database import get_session
from src.models.farmModel import Farm
from src.schemas.farmSchema import FarmSchema, UpdateFarmSchema


def createFarm(farm:  FarmSchema, session: Session = Depends(get_session) ):
    # Validación de los campos de texto como antes
    if not farm.nombre.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm name cannot be empty or only spaces.")
    if not farm.ubicacion.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location cannot be empty or only spaces.")
    
    # Validación del largo de nombre y ubicación como antes
    if len(farm.nombre) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm name must be at most 50 characters.")
    if farm.ubicacion and len(farm.ubicacion) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must be at most 50 characters.")
    
    # Validación de que los campos de texto no contengan caracteres especiales

    if not farm.ubicacion.replace(" ", "").isalpha():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farm location must only contain letters."
        )
    
    # Aquí solo validamos los campos numéricos a través de los esquemas sin hacer conversiones manuales
    newFarm = Farm(nombre = farm.nombre, ubicacion = farm.ubicacion, area_total = farm.area_total, latitud= farm.latitud, longitud = farm.longitud)

    session.add(newFarm)
    session.commit()
    session.refresh(newFarm)
    
    return {"msg": "Finca creada satisfactoriamente", "finca": newFarm}


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
    # Validación de los campos de texto como antes

    if farm_data.ubicacion is not None:
        if not farm_data.ubicacion.replace(" ", "").isalpha():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must only contain letters and spaces.")
    
    # Aplicar restricciones si se proporciona 'nombre'
    if farm_data.nombre is not None:
        farm_data.nombre = farm_data.nombre.strip()  # Eliminar espacios
        if len(farm_data.nombre) == 0:
            farm_data.nombre = None  # Tratar como vacío si solo tiene espacios
        if farm_data.nombre is not None and len(farm_data.nombre) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm_data.nombre must be at most 50 characters.")
    
    # Aplicar restricciones si se proporciona 'ubicacion'
    if farm_data.ubicacion is not None:
        farm_data.ubicacion = farm_data.ubicacion.strip()  # Eliminar espacios
        if len(farm_data.ubicacion) == 0:
            farm_data.ubicacion = None  # Tratar como vacío si solo tiene espacios
        if farm_data.ubicacion is not None and len(farm_data.ubicacion) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must be at most 50 characters.")
    
    # Obtener la finca existente
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )

    # Actualizar valores numéricos (latitud, longitud, área total) que ya han sido validados
    farm.area_total = farm_data.area_total if farm_data.area_total is not None else farm.area_total
    farm.latitud = farm_data.latitud if farm_data.latitud is not None else farm.latitud
    farm.longitud = farm_data.longitud if farm_data.longitud is not None else farm.longitud

    # Actualizar los campos de texto
    farm.nombre = farm_data.nombre
    farm.ubicacion = farm_data.ubicacion

    session.commit()
    session.refresh(farm)

    return {"msg": "Finca actualizada satisfactoriamente", "finca": farm}

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
