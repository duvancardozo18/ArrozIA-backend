from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.cultivoModel import Cultivo
from src.schemas.cultivoSchema import CultivoCreate, CultivoUpdate


def create_cultivo(cultivo: CultivoCreate, db: Session):
    db_cultivo = Cultivo(
        nombre_cultivo=cultivo.nombre_cultivo,
        variedad_id=cultivo.variedad_id,
        lote_id=cultivo.lote_id,
        fecha_siembra=cultivo.fecha_siembra,
        fecha_estimada_cosecha=cultivo.fecha_estimada_cosecha,
        fecha_real_cosecha=cultivo.fecha_real_cosecha,
        cantidad_cosechada=cultivo.cantidad_cosechada,
        unidad_peso_id=cultivo.unidad_peso_id,
        ingresos=cultivo.ingresos
    )
    
    db.add(db_cultivo)
    db.commit()
    db.refresh(db_cultivo)
    
    return db_cultivo

def get_cultivo(cultivo_id: int, db: Session):
    cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo not found")
    return cultivo

def get_all_cultivos(db: Session):
    cultivos = db.query(Cultivo).all()
    return cultivos

def update_cultivo(cultivo_id: int, cultivo_update: CultivoUpdate, db: Session):
    cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo not found")
    
    for key, value in cultivo_update.dict(exclude_unset=True).items():
        setattr(cultivo, key, value)
    
    db.commit()
    db.refresh(cultivo)
    return cultivo

def delete_cultivo(cultivo_id: int, db: Session):
    cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo not found")
    
    db.delete(cultivo)
    db.commit()
    return {"message": "Cultivo deleted successfully"}
