from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.soilAnalysisController import (
    create_soil_analysis,
    get_soil_analysis,
    get_all_soil_analyses,
    update_soil_analysis,
    delete_soil_analysis
)
from src.database.database import get_db
from src.schemas.soilAnalysisSchema import SoilAnalysisCreate, SoilAnalysisUpdate, SoilAnalysisOut

SOIL_ANALYSIS_ROUTES = APIRouter()

# Crear un nuevo análisis edafológico
@SOIL_ANALYSIS_ROUTES.post("/soil-analyses/", response_model=SoilAnalysisOut)
def create_soil_analysis_route(analysis: SoilAnalysisCreate, db: Session = Depends(get_db)):
    return create_soil_analysis(db, analysis)

# Obtener un análisis edafológico por ID
@SOIL_ANALYSIS_ROUTES.get("/soil-analyses/{analysis_id}", response_model=SoilAnalysisOut)
def get_soil_analysis_route(analysis_id: int, db: Session = Depends(get_db)):
    return get_soil_analysis(db, analysis_id)

# Listar todos los análisis edafológicos
@SOIL_ANALYSIS_ROUTES.get("/soil-analyses/", response_model=list[SoilAnalysisOut])
def list_soil_analyses_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_soil_analyses(db, skip, limit)

# Actualizar un análisis edafológico
@SOIL_ANALYSIS_ROUTES.put("/soil-analyses/{analysis_id}", response_model=SoilAnalysisOut)
def update_soil_analysis_route(analysis_id: int, analysis_update: SoilAnalysisUpdate, db: Session = Depends(get_db)):
    return update_soil_analysis(db, analysis_id, analysis_update)

# Eliminar un análisis edafológico
@SOIL_ANALYSIS_ROUTES.delete("/soil-analyses/{analysis_id}")
def delete_soil_analysis_route(analysis_id: int, db: Session = Depends(get_db)):
    return delete_soil_analysis(db, analysis_id)
