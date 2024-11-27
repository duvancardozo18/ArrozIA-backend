from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.weatherRecordModel import WeatherRecord
from src.schemas.weatherRecordSchema import WeatherRecordCreate, WeatherRecordResponse, LoteIdWithCoordinatesRequest
from src.controller.weatherRecordController import (
    createWeatherRecord,
    fetchWeatherRecord,
    getWeatherRecommendations,
    fetchWeatherHistory,
    createManualWeatherRecord,
    createWeatherRecordFromAPI,
    fetchWeatherRecordDetail
)

WEATHER_RECORD_ROUTES = APIRouter()

@WEATHER_RECORD_ROUTES.post("/weather-record/", response_model=WeatherRecordResponse)
def registerWeatherRecord(
    record: WeatherRecordCreate, db: Session = Depends(get_db)):
    return createWeatherRecord(db, record)

# @WEATHER_RECORD_ROUTES.post("/meteorology/manual", response_model=WeatherRecordResponse)
# def registerManualWeatherRecord(
#     record: WeatherRecordCreate, db: Session = Depends(get_db)):
#     return createManualWeatherRecord(db, record)

@WEATHER_RECORD_ROUTES.post("/meteorology/manual/{lote_id}", response_model=WeatherRecordResponse)
def registerManualWeatherRecord(
    lote_id: int,  # Tomamos el lote_id como parámetro
    record: WeatherRecordCreate,  # Los datos meteorológicos
    db: Session = Depends(get_db)
):
    # Aquí llamamos a la función que crea el registro meteorológico, pasando el lote_id
    return createManualWeatherRecord(db, record, lote_id)

@WEATHER_RECORD_ROUTES.post("/meteorology/api", response_model=WeatherRecordResponse)
def registerWeatherRecordFromAPI(data: LoteIdWithCoordinatesRequest, db: Session = Depends(get_db)):
    """
    Endpoint para registrar automáticamente un dato meteorológico basado en la API.
    """
    return createWeatherRecordFromAPI(db, data.lote_id, data.latitud, data.longitud)

@WEATHER_RECORD_ROUTES.get("/weather-record/{lote_id}/recommendations")
def getRecommendations(lote_id: int, db: Session = Depends(get_db)):
    return getWeatherRecommendations(db, lote_id)

@WEATHER_RECORD_ROUTES.get("/weather-record/by-date/{fecha}/{lote_id}", response_model=WeatherRecordResponse)
def getWeatherRecord(fecha: str, lote_id: int, db: Session = Depends(get_db)):
    record = fetchWeatherRecord(db, fecha, lote_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@WEATHER_RECORD_ROUTES.get("/meteorology/history/{lote_id}", response_model=List[WeatherRecordResponse])
def getWeatherHistory(
    lote_id: int,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    fuente_datos: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint para consultar el historial meteorológico de un lote.
    """
    return fetchWeatherHistory(db, lote_id, fecha_inicio, fecha_fin, fuente_datos)

@WEATHER_RECORD_ROUTES.get("/meteorology/history/detail/{id}", response_model=WeatherRecordResponse)
def getWeatherRecordDetail(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para ver el detalle de un registro meteorológico específico.
    """
    record = fetchWeatherRecordDetail(db, id)
    if record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@WEATHER_RECORD_ROUTES.put("/meteorology/history/update/{id}", response_model=WeatherRecordResponse)
def updateWeatherRecord(
    id: int,
    record: WeatherRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un registro meteorológico existente.
    """
    existing_record = db.query(WeatherRecord).filter(WeatherRecord.id == id).first()
    if existing_record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Actualizar los campos del registro existente
    for key, value in record.dict(exclude_unset=True).items():
        setattr(existing_record, key, value)

    # Asignar valor por defecto a 'fuente_datos' si está vacío
    if existing_record.fuente_datos is None:
        existing_record.fuente_datos = "manual"

    db.commit()
    db.refresh(existing_record)
    return existing_record
