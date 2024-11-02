from pydantic import BaseModel
from datetime import date, time
from typing import Optional, Union, Any

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
    hora: time
    temperatura: float
    presion_atmosferica: float
    humedad: float
    precipitacion: Optional[float] = None
    indice_ultravioleta: float
    horas_sol: float
    fuente_datos: Optional[str]  # Ahora acepta None
    api_respuesta: Optional[Union[dict, Any]] = None  # Para el campo JSON

    class Config:
        orm_mode = True
