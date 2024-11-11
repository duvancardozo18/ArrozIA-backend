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

# Función para calcular el arriendo total del lote en función de la duración del cultivo
def calculate_total_rent(plot_id: int, session: Session):
    # Buscar el lote en la base de datos
    land = session.query(Land).filter(Land.id == plot_id).first()
    if not land:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El lote especificado no existe."
        )
    
    # Calcular el tiempo que dura el cultivo (puedes ajustar esto según tus datos)
    cultivo = session.query(Crop).filter(Crop.plotId == plot_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cultivo especificado no existe."
        )
    tiempo_cultivo = (cultivo.estimatedHarvestDate - cultivo.plantingDate).days / 30  # Meses aproximados

    # Calcular el arriendo total
    total_rent = land.arriendo_real * tiempo_cultivo if land.arriendo_real else 0
    
    return {"total_rent": total_rent}

# Calcular costos de maquinaria y mano de obra cultural
def calculate_machinery_and_labor_costs(plot_id: int, session: Session):
    tasks = session.query(Task).filter(Task.cultivo_id == plot_id).all()

    print(f"Tasks for plot_id {plot_id}: {[task.id for task in tasks]}")  # Imprime todas las tareas encontradas

    total_machinery_cost = 0.0
    total_labor_cost = 0.0

    for task in tasks:
        print(f"Processing Task ID: {task.id}, Machinery ID: {task.maquinaria_agricola_id}, Labor ID: {task.labor_cultural_id}")

        # Verificar y calcular el costo de maquinaria
        if task.maquinaria_agricola_id:
            maquinaria = session.query(Machinery).filter(Machinery.id == task.maquinaria_agricola_id).first()
            if maquinaria:
                task_cost = maquinaria.costPerHour * task.tiempo_hora  # Cambiado a costPerHour
                print(f"Machinery Cost for Task ID {task.id}: {task_cost}")
                total_machinery_cost += task_cost

        # Verificar y calcular el costo de labor cultural
        if task.labor_cultural_id:
            labor = session.query(LaborCultural).filter(LaborCultural.id == task.labor_cultural_id).first()
            if labor:
                labor_cost = labor.precio_hora_real * task.tiempo_hora
                print(f"Labor Cost for Task ID {task.id}: {labor_cost}")
                total_labor_cost += labor_cost

    print(f"Total Machinery Cost: {total_machinery_cost}")
    print(f"Total Labor Cost: {total_labor_cost}")
    return {
        "total_machinery_cost": total_machinery_cost,
        "total_labor_cost": total_labor_cost
    }

# Calcular costos de insumos agrícolas en función de la cantidad
def calculate_agricultural_input_costs(plot_id: int, session: Session):
    agricultural_inputs = session.query(AgriculturalInput).join(Crop).filter(Crop.plotId == plot_id).all()
    total_input_cost = sum(
        [input.unit_cost_real * input.quantity for input in agricultural_inputs if input]
    )
    return {"total_input_cost": total_input_cost}

# Calcular costos de insumos agrícolas en función de la cantidad para un lote específico
def calculate_agricultural_input_costs(plot_id: int, session: Session):
    # Obtener los cultivos asociados al lote especificado
    cultivos = session.query(Crop).filter(Crop.plotId == plot_id).all()

    total_input_cost = 0
    # Iterar sobre cada cultivo y sumar los costos de insumos asociados
    for cultivo in cultivos:
        agricultural_inputs = session.query(AgriculturalInput).filter(AgriculturalInput.cultivo_id == cultivo.id).all()
        
        for input in agricultural_inputs:
            total_input_cost += input.costo_unitario * input.cantidad

    return {"total_input_cost": total_input_cost}