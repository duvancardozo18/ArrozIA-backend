from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.weatherRecordSchema import WeatherRecordCreate, WeatherRecordResponse
from src.controller.weatherRecordController import (
    createWeatherRecord,
    fetchWeatherRecord,
    getWeatherRecommendations,
    fetchWeatherHistory
)

WEATHER_RECORD_ROUTES = APIRouter()

@WEATHER_RECORD_ROUTES.post("/weather-record/", response_model=WeatherRecordResponse)
def registerWeatherRecord(
    record: WeatherRecordCreate, db: Session = Depends(get_db)):
    return createWeatherRecord(db, record)

@WEATHER_RECORD_ROUTES.get("/weather-record/{lote_id}/recommendations")
def getRecommendations(lote_id: int, db: Session = Depends(get_db)):
    return getWeatherRecommendations(db, lote_id)

@WEATHER_RECORD_ROUTES.get("/weather-record/by-date/{fecha}/{lote_id}", response_model=WeatherRecordResponse)
def getWeatherRecord(fecha: str, lote_id: int, db: Session = Depends(get_db)):
    record = fetchWeatherRecord(db, fecha, lote_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@WEATHER_RECORD_ROUTES.get("/weather-records/history/{lote_id}", response_model=List[WeatherRecordResponse])
def getWeatherRecordHistory(
    lote_id: int,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    return fetchWeatherHistory(db, lote_id, start_date, end_date)
