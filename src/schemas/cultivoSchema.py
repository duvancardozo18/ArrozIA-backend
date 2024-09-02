from pydantic import BaseModel
from datetime import date
from typing import Optional

class CultivoBase(BaseModel):
    nombre_cultivo: str
    variedad_id: int
    lote_id: int
    fecha_siembra: date
    fecha_estimada_cosecha: date
    fecha_real_cosecha: Optional[date]
    cantidad_cosechada: Optional[float]
    unidad_peso_id: int
    ingresos: Optional[float]

class CultivoCreate(CultivoBase):
    pass

class CultivoUpdate(BaseModel):
    nombre_cultivo: Optional[str]
    variedad_id: Optional[int]
    lote_id: Optional[int]
    fecha_siembra: Optional[date]
    fecha_estimada_cosecha: Optional[date]
    fecha_real_cosecha: Optional[date]
    cantidad_cosechada: Optional[float]
    unidad_peso_id: Optional[int]
    ingresos: Optional[float]

class CultivoOut(CultivoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
