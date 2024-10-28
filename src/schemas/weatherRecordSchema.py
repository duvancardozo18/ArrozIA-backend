from pydantic import BaseModel
from datetime import date
from typing import Optional

class WeatherRecordCreate(BaseModel):
    fecha: date
    temperatura: float
    presion_atmosferica: float
    humedad: float
    precipitacion: Optional[float] = None
    indice_ultravioleta: float
    horas_sol: float
    lote_id: int

class WeatherRecordResponse(WeatherRecordCreate):
    id: int
