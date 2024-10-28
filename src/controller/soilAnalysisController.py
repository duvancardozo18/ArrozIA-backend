from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.soilAnalysisModel import SoilAnalysis
from src.schemas.soilAnalysisSchema import SoilAnalysisCreate, SoilAnalysisUpdate

def create_soil_analysis(db: Session, analysis: SoilAnalysisCreate):
    new_analysis = SoilAnalysis(**analysis.dict())
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

def get_soil_analysis(db: Session, analysis_id: int):
    analysis = db.query(SoilAnalysis).filter(SoilAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    return analysis

def get_all_soil_analyses(db: Session, skip: int = 0, limit: int = 10):
    analyses = db.query(SoilAnalysis).offset(skip).limit(limit).all()
    if not analyses:
        raise HTTPException(status_code=404, detail="No se encontraron análisis")
    return analyses

def update_soil_analysis(db: Session, analysis_id: int, analysis_update: SoilAnalysisUpdate):
    analysis = get_soil_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado para actualización")
    for key, value in analysis_update.dict(exclude_unset=True).items():
        setattr(analysis, key, value)
    db.commit()
    db.refresh(analysis)
    return analysis

def delete_soil_analysis(db: Session, analysis_id: int):
    analysis = get_soil_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado para eliminación")
    db.delete(analysis)
    db.commit()
    return {"message": "Análisis edafológico eliminado correctamente"}
