from pydantic import BaseModel
from datetime import date, time
from typing import Optional, Union, Any

# Modelo para recibir la información de la finca con latitud y longitud
class LoteIdWithCoordinatesRequest(BaseModel):
    lote_id: int
    latitud: float
    longitud: float

    class Config:
        orm_mode = True

class WeatherRecordCreate(BaseModel):
    lote_id: Optional[int] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    temperatura: Optional[float] = None
    presion_atmosferica: Optional[float] = None
    humedad: Optional[float] = None
    precipitacion: Optional[float] = None
    indice_ultravioleta: Optional[float] = None
    horas_sol: Optional[float] = None

    class Config:
        orm_mode = True

class WeatherRecordResponse(BaseModel):
    id: int
    lote_id: int
    fecha: date
    hora: Optional[time] = None  # Cambiado a Optional para aceptar None
    temperatura: float
    presion_atmosferica: float
    humedad: float
    precipitacion: Optional[float] = None
    indice_ultravioleta: float
    horas_sol: float
    fuente_datos: Optional[str] = None  # Acepta None
    api_respuesta: Optional[Union[dict, Any]] = None  # Para el campo JSON

    class Config:
        orm_mode = True
