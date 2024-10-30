from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.monitoringModel import Monitoring
from src.schemas.monitoringSchema import MonitoringCreate, MonitoringUpdate
from src.models.riceVarStageModel import RiceVarStageModel

def create_monitoring(db: Session, monitoring: MonitoringCreate):
    if monitoring.variedad_arroz_etapa_fenologica_id is not None:
        # Verificar si el ID de la variedad de arroz existe en la tabla correspondiente
        if not db.query(RiceVarStageModel).filter(RiceVarStageModel.id == monitoring.variedad_arroz_etapa_fenologica_id).first():
            raise HTTPException(status_code=400, detail="ID de variedad de arroz no válida")

        db_monitoring = Monitoring(**monitoring.dict())
        db.add(db_monitoring)
        db.commit()
        db.refresh(db_monitoring)
        return db_monitoring
    else:
        raise HTTPException(status_code=400, detail="ID de variedad de arroz es necesario")

def get_monitoring(db: Session, monitoring_id: int):
    db_monitoring = db.query(Monitoring).filter(Monitoring.id == monitoring_id).first()
    if db_monitoring is None:
        raise HTTPException(status_code=404, detail="Monitoreo no encontrado")
    return db_monitoring

def get_monitorings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Monitoring).offset(skip).limit(limit).all()

def update_monitoring(db: Session, monitoring_id: int, monitoring: MonitoringUpdate):
    db_monitoring = db.query(Monitoring).filter(Monitoring.id == monitoring_id).first()
    if db_monitoring is None:
        raise HTTPException(status_code=404, detail="Monitoreo no encontrado")
    
    for key, value in monitoring.dict(exclude_unset=True).items():
        setattr(db_monitoring, key, value)
    db.commit()
    db.refresh(db_monitoring)
    return db_monitoring

def delete_monitoring(db: Session, monitoring_id: int):
    db_monitoring = db.query(Monitoring).filter(Monitoring.id == monitoring_id).first()
    if db_monitoring is None:
        raise HTTPException(status_code=404, detail="Monitoreo no encontrado")
    
    db.delete(db_monitoring)
    db.commit()
    return {"message": "Monitoreo eliminado correctamente"}
