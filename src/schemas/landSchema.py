from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class LandSchema(BaseModel):
    id: Optional[int] = None
    nombre: str
    finca_id: int
    finca_nombre: Optional[str] = None  # Nuevo campo para incluir el nombre de la finca
    area: float
    latitud: Optional[Decimal]  
    longitud: Optional[Decimal] 

    class Config:
        orm_mode = True
        schema_extra = {
            'latitud': condecimal(max_digits=10, decimal_places=5),
            'longitud': condecimal(max_digits=10, decimal_places=5)
        }


class UpdateLandSchema(BaseModel):
    nombre: Optional[str] = None
    finca_id: Optional[int] = None
    area: Optional[float] = None
    unidad_area_id: Optional[int] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
