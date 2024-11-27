from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.landModel import Land
from src.schemas.landSchema import LandSchema, UpdateLandSchema
from src.models.laborCulturalModel import LaborCultural
from datetime import datetime
from src.models.cropModel import Crop
from src.models.taskModel import Task
from src.models.machineryModel import Machinery
from src.models.agriculturalInputModel import AgriculturalInput

# Función para generar slugs basados en el nombre
def generate_slug(name: str) -> str:
    return name.lower().replace(" ", "-")

# Crear lote (Land) con slug
def createLand(land: LandSchema, session: Session = Depends(get_session)):
    slug = generate_slug(land.nombre)
    newLand = Land(
        nombre=land.nombre,
        finca_id=land.finca_id,
        area=land.area,
        latitud=land.latitud,
        longitud=land.longitud,
        slug=slug
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

# Obtener un lote por su ID, incluyendo el nombre de la finca
def getLandById(land_id: int, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )
    finca_name = land.finca.nombre if land.finca else "Finca desconocida"
    return {
        "id": land.id,
        "nombre": land.nombre,
        "finca_id": land.finca_id,
        "finca_nombre": finca_name,
        "area": land.area,
        "latitud": land.latitud,
        "longitud": land.longitud,
        "slug": land.slug
    }

# Actualizar un lote
def updateLand(land_id: int, land_data: UpdateLandSchema, session: Session = Depends(get_session)):
    land = session.query(Land).filter(Land.id == land_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lote con id {land_id} no encontrado"
        )
    update_data = land_data.dict(exclude_unset=True)
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

# Calcular el arriendo total del lote
def calculate_total_rent(plot_id: int, session: Session):
    land = session.query(Land).filter(Land.id == plot_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El lote especificado no existe."
        )
    cultivo = session.query(Crop).filter(Crop.plotId == plot_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cultivo especificado no existe."
        )
    tiempo_cultivo = (cultivo.estimatedHarvestDate - cultivo.plantingDate).days / 30
    total_rent = land.arriendo_real * tiempo_cultivo if land.arriendo_real else 0
    return {"total_rent": total_rent}

# Calcular costos de maquinaria y mano de obra cultural
def calculate_machinery_and_labor_costs(plot_id: int, session: Session):
    tasks = session.query(Task).filter(Task.cultivo_id == plot_id).all()
    total_machinery_cost = 0.0
    total_labor_cost = 0.0
    for task in tasks:
        if task.maquinaria_agricola_id:
            maquinaria = session.query(Machinery).filter(Machinery.id == task.maquinaria_agricola_id).first()
            if maquinaria:
                total_machinery_cost += maquinaria.costPerHour * task.tiempo_hora
        if task.labor_cultural_id:
            labor = session.query(LaborCultural).filter(LaborCultural.id == task.labor_cultural_id).first()
            if labor:
                total_labor_cost += labor.precio_hora_real * task.tiempo_hora
    return {
        "total_machinery_cost": total_machinery_cost,
        "total_labor_cost": total_labor_cost
    }

# Calcular costos de insumos agrícolas
def calculate_agricultural_input_costs(plot_id: int, session: Session):
    cultivos = session.query(Crop).filter(Crop.plotId == plot_id).all()
    total_input_cost = 0
    for cultivo in cultivos:
        agricultural_inputs = session.query(AgriculturalInput).filter(AgriculturalInput.cultivo_id == cultivo.id).all()
        for input in agricultural_inputs:
            total_input_cost += input.costo_unitario * input.cantidad
    return {"total_input_cost": total_input_cost}
