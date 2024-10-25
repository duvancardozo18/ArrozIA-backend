from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.schemas.machinerySchema import MaquinariaAgricolaCreate, MaquinariaAgricolaUpdate
from src.models.machineryModel import Machinery

# Crear una nueva maquinaria
def create_machinery(machinery: MaquinariaAgricolaCreate, db: Session):
    # Verificar si ya existe una maquinaria con el mismo nombre
    existing_machinery = db.query(Machinery).filter(Machinery.name == machinery.name).first()
    if existing_machinery:
        raise HTTPException(status_code=400, detail="Ya existe una maquinaria con el mismo nombre")
    
    # Crear la nueva maquinaria si no existe
    db_machinery = Machinery(**machinery.dict())
    db.add(db_machinery)
    db.commit()
    db.refresh(db_machinery)
    return db_machinery

# Obtener una maquinaria por ID
def get_machinery(machinery_id: int, db: Session):
    machinery = db.query(Machinery).filter(Machinery.id == machinery_id).first()
    if not machinery:
        raise HTTPException(status_code=404, detail="Maquinaria no encontrada")
    return machinery

# Obtener todas las maquinarias
def get_all_machineries(db: Session):
    machineries = db.query(Machinery).all()
    if not machineries:
        raise HTTPException(status_code=404, detail="No se encontraron maquinarias")
    return machineries

# Actualizar una maquinaria por ID
def update_machinery(machinery_id: int, machinery: MaquinariaAgricolaUpdate, db: Session):
    db_machinery = db.query(Machinery).filter(Machinery.id == machinery_id).first()
    if not db_machinery:
        raise HTTPException(status_code=404, detail="Maquinaria no encontrada")

    # Actualizar solo los campos que se hayan proporcionado
    for key, value in machinery.dict(exclude_unset=True).items():
        setattr(db_machinery, key, value)
    db.commit()
    db.refresh(db_machinery)
    return db_machinery

# Eliminar una maquinaria por ID
def delete_machinery(machinery_id: int, db: Session):
    db_machinery = db.query(Machinery).filter(Machinery.id == machinery_id).first()
    if not db_machinery:
        raise HTTPException(status_code=404, detail="Maquinaria no encontrada")
    
    db.delete(db_machinery)
    db.commit()
    return {"message": "Maquinaria eliminada correctamente"}
