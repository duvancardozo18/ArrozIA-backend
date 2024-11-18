from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.database import get_db
from src.controller.culturalWorkController import (
    get_cultural_works_by_crop,
    get_total_cultural_works_value,
    filter_by_activity,
    filter_by_machinery,
    filter_by_operator,
    filter_by_date_range
)

router = APIRouter()
#lista totas las actividades del cultivo
@router.get("/crops/{cultivo_id}/cultural-works")
def list_cultural_works(cultivo_id: int, db: Session = Depends(get_db)):
    return get_cultural_works_by_crop(db, cultivo_id)

#valor total de todas las actividades
@router.get("/crops/{cultivo_id}/cultural-works/total-value")
def get_total_value(cultivo_id: int, db: Session = Depends(get_db)):
    return get_total_cultural_works_value(db, cultivo_id)

#filtro por actividad
@router.get("/crops/{cultivo_id}/cultural-works/filter-by-activity")
def filter_activity(cultivo_id: int, activity_name: str, db: Session = Depends(get_db)):
    return filter_by_activity(cultivo_id, activity_name, db)

#filtro por maquinaria
@router.get("/crops/{cultivo_id}/cultural-works/filter-by-machinery")
def filter_machinery(cultivo_id: int, machinery_name: str, db: Session = Depends(get_db)):
    return filter_by_machinery(cultivo_id, machinery_name, db)

#filtro por operador
@router.get("/crops/{cultivo_id}/cultural-works/filter-by-operator")
def filter_operator(cultivo_id: int, operator_name: str, db: Session = Depends(get_db)):
    return filter_by_operator(cultivo_id, operator_name, db)

#filtro fecha
@router.get("/crops/{cultivo_id}/cultural-works/filter-by-date-range")
def filter_date_range(cultivo_id: int, start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    return filter_by_date_range(cultivo_id, start_date, end_date, db)
