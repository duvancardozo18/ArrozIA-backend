from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.monitoringModel import Monitoring
from src.schemas.monitoringSchema import MonitoringCreate, MonitoringUpdate, MonitoringOut  # Importa MonitoringOut
from src.models.varietyRiceStageModel import VarietyRiceStageModel
from src.models.cropModel import Crop
from src.models.phenologicalStageModel import PhenologicalStage

def create_monitoring(db: Session, monitoring: MonitoringCreate):
    if monitoring.variedad_arroz_etapa_fenologica_id is not None:
        # Verificar si el ID de la variedad de arroz existe en la tabla VarietyRiceStageModel
        if not db.query(VarietyRiceStageModel).filter(VarietyRiceStageModel.id == monitoring.variedad_arroz_etapa_fenologica_id).first():
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
    # Consulta los monitoreos junto con el nombre de la etapa fenológica
    monitorings = (
        db.query(Monitoring, PhenologicalStage.nombre.label("etapaNombre"))
        .join(PhenologicalStage, Monitoring.variedad_arroz_etapa_fenologica_id == PhenologicalStage.id, isouter=True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    # Retorna los resultados directamente usando el esquema MonitoringOut
    return [
        MonitoringOut(
            **monitoring[0].__dict__,  # Extrae atributos de Monitoring
            etapaNombre=monitoring.etapaNombre  # Incluye el nombre de la etapa
        )
        for monitoring in monitorings
    ]

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

def get_monitorings_by_crop(db: Session, crop_id: int):
    # Verifica si el cultivo existe
    if not db.query(Crop).filter(Crop.id == crop_id).first():
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")

    # Consulta con join para obtener el nombre de la etapa fenológica
    monitorings = (
        db.query(
            Monitoring,
            PhenologicalStage.nombre.label("etapaNombre")
        )
        .join(PhenologicalStage, Monitoring.variedad_arroz_etapa_fenologica_id == PhenologicalStage.id, isouter=True)
        .filter(Monitoring.crop_id == crop_id)
        .all()
    )
    
    return [
        MonitoringOut(
            **monitoring[0].__dict__,  # Extrae atributos de Monitoring
            etapaNombre=monitoring.etapaNombre  # Incluye el nombre de la etapa
        )
        for monitoring in monitorings
    ]
