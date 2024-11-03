from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.orm import Session
from src.controller.soilAnalysisController import (
    create_soil_analysis,
    get_analyses_by_lote,
    get_analysis_detail,
    update_soil_analysis,
    delete_soil_analysis
)
from src.schemas.soilAnalysisSchema import SoilAnalysisCreate, SoilAnalysisOut, SoilAnalysisSimpleOut
from src.database.database import get_db

SOIL_ANALYSIS_ROUTES = APIRouter()

@SOIL_ANALYSIS_ROUTES.post("/soil_analysis", response_model=SoilAnalysisSimpleOut, status_code=201)
def create_soil_analysis_route(
    soil_data: SoilAnalysisCreate = Body(...),
    db: Session = Depends(get_db)
):
    # Crear el análisis de suelo y obtener el ID
    analysis = create_soil_analysis(soil_data, db)
    
    # Crear la respuesta simplificada con el ID y mensaje
    response_data = SoilAnalysisSimpleOut(
        id=analysis.id,
        message=f"Análisis de suelo creado exitosamente con el id: {analysis.id}"
    )
    
    return response_data

@SOIL_ANALYSIS_ROUTES.get("/soil_analysis/{lote_id}")
def get_analyses_by_lote_route(lote_id: int, db: Session = Depends(get_db)):
    return get_analyses_by_lote(lote_id, db)

@SOIL_ANALYSIS_ROUTES.get("/soil_analysis/{lote_id}/{analysis_id}", response_model=SoilAnalysisOut)
def get_analysis_detail_route(lote_id: int, analysis_id: int, db: Session = Depends(get_db)):
    return get_analysis_detail(lote_id, analysis_id, db)

@SOIL_ANALYSIS_ROUTES.put("/soil_analysis/{lote_id}/{analysis_id}")
def update_soil_analysis_route(lote_id: int, analysis_id: int, soil_data: SoilAnalysisCreate, db: Session = Depends(get_db)):
    return update_soil_analysis(lote_id, analysis_id, soil_data, db)

@SOIL_ANALYSIS_ROUTES.delete("/soil_analysis/{lote_id}/{analysis_id}")
def delete_soil_analysis_route(lote_id: int, analysis_id: int, db: Session = Depends(get_db)):
    return delete_soil_analysis(lote_id, analysis_id, db)
