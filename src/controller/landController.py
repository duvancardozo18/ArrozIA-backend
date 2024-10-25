from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.landModel import Land
from src.schemas.landSchema import LandSchema, UpdateLandSchema


# Función para generar slugs basados en el nombre
def generate_slug(name: str) -> str:
    return name.lower().replace(" ", "-")

# Crear lote (Land) con slug
def createLand(land: LandSchema, session: Session = Depends(get_session)):
    # Generar el slug a partir del nombre del lote
    slug = generate_slug(land.nombre)
    
    # Crear el nuevo lote con los datos recibidos y el slug generado
    newLand = Land(
        nombre=land.nombre, 
        finca_id=land.finca_id, 
        area=land.area, 
        latitud=land.latitud, 
        longitud=land.longitud, 
        slug=slug  # Asigna el slug generado al lote
    )
    
    session.add(newLand)
    session.commit()
    session.refresh(newLand)
    
    return {
        "msg": "Lote creado satisfactoriamente", 
        "slug": newLand.slug
    }

# Obtener todos los lotes
def getAllLands(session: Session = Depends(get_session)):
    lands = session.query(Land).all()
    return lands

# Obtener un lote por su ID
def getLandById(land_id: int, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )
    return land

# Actualizar un lote
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

# Eliminar un lote
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
