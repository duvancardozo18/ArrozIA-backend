from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from src.models.laborCulturalModel import LaborCultural
from src.schemas.laborCulturalSchema import LaborCulturalCreate, LaborCulturalUpdate


# Función auxiliar para obtener una labor cultural por ID
def _get_labor_cultural_or_404(labor_id: int, db: Session) -> LaborCultural:
    labor = db.query(LaborCultural).filter(LaborCultural.id == labor_id).first()
    if not labor:
        raise HTTPException(status_code=404, detail=f"Labor cultural con ID {labor_id} no encontrada")
    return labor


# Crear una nueva labor cultural
def create_labor_cultural(labor_data: LaborCulturalCreate, db: Session):
    try:
        labor = LaborCultural(**labor_data.dict())
        db.add(labor)
        db.commit()
        db.refresh(labor)
        return labor
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la labor cultural: {str(e)}")


# Obtener todas las labores culturales
def get_labores_culturales(db: Session):
    try:
        return db.query(LaborCultural).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las labores culturales: {str(e)}")


# Obtener una labor cultural por ID
def get_labor_cultural_by_id(labor_id: int, db: Session):
    return _get_labor_cultural_or_404(labor_id, db)


# Actualizar una labor cultural existente
def update_labor_cultural(labor_id: int, labor_data: LaborCulturalUpdate, db: Session):
    try:
        labor = _get_labor_cultural_or_404(labor_id, db)
        for key, value in labor_data.dict(exclude_unset=True).items():
            setattr(labor, key, value)
        db.commit()
        db.refresh(labor)
        return labor
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la labor cultural: {str(e)}")


# Eliminar una labor cultural existente
def delete_labor_cultural(labor_id: int, db: Session):
    try:
        labor = _get_labor_cultural_or_404(labor_id, db)
        db.delete(labor)
        db.commit()
        return {"message": f"Labor cultural con ID {labor_id} eliminada con éxito"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la labor cultural: {str(e)}")
