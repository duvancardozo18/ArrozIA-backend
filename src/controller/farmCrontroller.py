from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.farmModel import Farm
from src.schemas.farmSchema import FarmSchema, UpdateFarmSchema

def createFarm(farm: FarmSchema, session: Session = Depends(get_session)):
    print(f"Datos recibidos: {farm}")
    
    # Validación de los campos de texto
    if not farm.nombre.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm name cannot be empty or only spaces.")
    
    # Verificar si ubicacion no es None antes de usar .strip()
    if farm.ubicacion and not farm.ubicacion.strip():  # Si ubicacion existe y es vacía o tiene solo espacios
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location cannot be empty or only spaces.")
    
    # Validación del largo de nombre y ubicación
    if len(farm.nombre) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm name must be at most 50 characters.")
    if farm.ubicacion and len(farm.ubicacion) > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must be at most 100 characters.")
    
    # Validación de que los campos de texto no contengan caracteres especiales
    if farm.ubicacion and not farm.ubicacion.replace(" ", "").isalpha():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farm location must only contain letters."
        )

    # Crear nueva instancia de la finca con todos los campos
    newFarm = Farm(
        nombre=farm.nombre,
        ubicacion=farm.ubicacion,
        area_total=farm.area_total,
        latitud=farm.latitud,
        longitud=farm.longitud,
        slug=farm.slug,
        ciudad=farm.ciudad,
        departamento=farm.departamento,
        pais=farm.pais
    )

    session.add(newFarm)
    session.commit()
    session.refresh(newFarm)
    
    return {"msg": "Finca creada satisfactoriamente", "finca": newFarm}


def getAllFarms(session: Session = Depends(get_session)):
    farms = session.query(Farm).all()
    farms_list = [
        {
            "id": farm.id,
            "nombre": farm.nombre,
            "ubicacion": farm.ubicacion if farm.ubicacion else "",
            "area_total": farm.area_total if farm.area_total is not None else 0.0,
            "latitud": farm.latitud,
            "longitud": farm.longitud,
            "ciudad": farm.ciudad,
            "departamento": farm.departamento,
            "pais": farm.pais
        }
        for farm in farms
    ]
    return farms_list

def getFarmById(farm_id: int, session: Session = Depends(get_session)):
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )
    return farm

def updateFarm(farm_id: int, farm_data: UpdateFarmSchema, session: Session = Depends(get_session)):
    # Validación de los campos de texto
    if farm_data.ubicacion is not None:
        if not farm_data.ubicacion.replace(" ", "").isalpha():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must only contain letters and spaces.")
    
    if farm_data.nombre is not None:
        farm_data.nombre = farm_data.nombre.strip()
        if len(farm_data.nombre) == 0:
            farm_data.nombre = None
        if farm_data.nombre is not None and len(farm_data.nombre) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Farm name must be at most 50 characters.")
    
    if farm_data.ubicacion is not None:
        farm_data.ubicacion = farm_data.ubicacion.strip()
        if len(farm_data.ubicacion) == 0:
            farm_data.ubicacion = None
        if farm_data.ubicacion is not None and len(farm_data.ubicacion) > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location must be at most 100 characters.")
    
    farm = session.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Finca con id {farm_id} no encontrada"
        )

    # Actualizar valores
    farm.nombre = farm_data.nombre if farm_data.nombre is not None else farm.nombre
    farm.ubicacion = farm_data.ubicacion if farm_data.ubicacion is not None else farm.ubicacion
    farm.area_total = farm_data.area_total if farm_data.area_total is not None else farm.area_total
    farm.latitud = farm_data.latitud if farm_data.latitud is not None else farm.latitud
    farm.longitud = farm_data.longitud if farm_data.longitud is not None else farm.longitud
    farm.ciudad = farm_data.ciudad if farm_data.ciudad is not None else farm.ciudad
    farm.departamento = farm_data.departamento if farm_data.departamento is not None else farm.departamento
    farm.pais = farm_data.pais if farm_data.pais is not None else farm.pais

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
