from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import join
from src.models.harvestModel import Harvest
from src.models.cropModel import Crop

def get_all_harvests_by_crop(db: Session, cultivo_id: int):
    # Obtener la información del cultivo
    crop = db.query(Crop.id, Crop.cropName).filter(Crop.id == cultivo_id).first()
    if not crop:
        raise ValueError(f"Crop with ID {cultivo_id} does not exist.")

    # Obtener el listado de cosechas
    harvests = (
        db.query(
            Harvest.id,
            Harvest.cultivo_id,
            Harvest.fecha_estimada_cosecha,
            Harvest.fecha_cosecha,
            Harvest.precio_carga_mercado,
            Harvest.gasto_transporte_cosecha,
            Harvest.gasto_recoleccion,
            Harvest.cantidad_producida_cosecha,
            Harvest.venta_cosecha,
        )
        .filter(Harvest.cultivo_id == cultivo_id)
        .all()
    )

    # Convertir resultados a listas de diccionarios
    harvests_list = [dict(harvest._mapping) for harvest in harvests]

    # Retornar el ID y nombre del cultivo junto con las cosechas
    return {
        "cultivo_id": crop.id,
        "cultivo_nombre": crop.cropName,
        "cosechas": harvests_list,
    }

def get_harvest(db: Session, cultivo_id: int, cosecha_id: int):
    harvest = (
        db.query(
            Harvest.id,
            Harvest.cultivo_id,
            Harvest.fecha_estimada_cosecha,
            Harvest.fecha_cosecha,
            Harvest.precio_carga_mercado,
            Harvest.gasto_transporte_cosecha,
            Harvest.gasto_recoleccion,
            Harvest.cantidad_producida_cosecha,
            Harvest.venta_cosecha,
            Crop.cropName.label("cultivo_nombre"),
        )
        .join(Crop, Crop.id == Harvest.cultivo_id)
        .filter(Harvest.cultivo_id == cultivo_id, Harvest.id == cosecha_id)
        .first()
    )
    if not harvest:
        raise ValueError(f"Harvest with ID {cosecha_id} not found for crop ID {cultivo_id}.")
    # Convert query result to a dictionary
    return dict(harvest._mapping)

def create_harvest(db: Session, harvest_data):
    # Validar que el cultivo exista
    cultivo = db.query(Crop).filter(Crop.id == harvest_data["cultivo_id"]).first()
    if not cultivo:
        raise ValueError(f"Crop with ID {harvest_data['cultivo_id']} does not exist.")

    # Crear la nueva cosecha
    new_harvest = Harvest(**harvest_data)
    db.add(new_harvest)
    db.commit()
    db.refresh(new_harvest)
    return new_harvest

def update_harvest(db: Session, cultivo_id: int, cosecha_id: int, update_data: dict):
    # Buscar la cosecha por cultivo_id y cosecha_id
    harvest = db.query(Harvest).filter(Harvest.cultivo_id == cultivo_id, Harvest.id == cosecha_id).first()
    if not harvest:
        raise HTTPException(status_code=404, detail=f"Harvest with ID {cosecha_id} not found for crop ID {cultivo_id}.")

    # Validar si el cultivo_id se quiere cambiar
    new_cultivo_id = update_data.get("cultivo_id")
    if new_cultivo_id and new_cultivo_id != cultivo_id:
        crop_exists = db.query(Crop).filter(Crop.id == new_cultivo_id).first()
        if not crop_exists:
            raise HTTPException(status_code=400, detail=f"Crop with ID {new_cultivo_id} does not exist.")

    # Actualizar los campos de la cosecha
    for key, value in update_data.items():
        if hasattr(harvest, key):
            setattr(harvest, key, value)

    # Guardar los cambios
    db.commit()
    db.refresh(harvest)
    return harvest

def delete_harvest(db: Session, cultivo_id: int, cosecha_id: int):
    # Validar que la cosecha exista
    harvest = db.query(Harvest).filter(Harvest.cultivo_id == cultivo_id, Harvest.id == cosecha_id).first()
    if not harvest:
        raise ValueError(f"Harvest with ID {cosecha_id} not found for crop ID {cultivo_id}.")

    # Eliminar la instancia de Harvest
    db.delete(harvest)
    db.commit()
    return {"message": "Harvest deleted successfully"}