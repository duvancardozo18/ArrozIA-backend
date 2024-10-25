from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from src.models.laborCulturalModel import LaborCultural
from src.schemas.laborCulturalSchema import LaborCulturalCreate, LaborCulturalUpdate, LaborCulturalResponse
from src.database.database import get_db

# Crear una nueva labor cultural
def create_labor_cultural(labor: LaborCulturalCreate, db: Session = Depends(get_db)):
    db_labor = LaborCultural(nombre=labor.nombre, descripcion=labor.descripcion)
    db.add(db_labor)
    db.commit()
    db.refresh(db_labor)
    return db_labor

# Consultar todas las labores culturales
def get_labores_culturales(db: Session = Depends(get_db)):
    return db.query(LaborCultural).all()

# Modificar una labor cultural existente
def update_labor_cultural(labor_id: int, labor: LaborCulturalUpdate, db: Session = Depends(get_db)):
    db_labor = db.query(LaborCultural).filter(LaborCultural.id == labor_id).first()
    if not db_labor:
        raise HTTPException(status_code=404, detail="Labor Cultural no encontrada")
    db_labor.nombre = labor.nombre
    db_labor.descripcion = labor.descripcion
    db.commit()
    db.refresh(db_labor)
    return db_labor

# Eliminar una labor cultural
def delete_labor_cultural(labor_id: int, db: Session = Depends(get_db)):
    db_labor = db.query(LaborCultural).filter(LaborCultural.id == labor_id).first()
    if not db_labor:
        raise HTTPException(status_code=404, detail="Labor Cultural no encontrada")
    db.delete(db_labor)
    db.commit()
    return {"detail": "Labor Cultural eliminada correctamente"}
