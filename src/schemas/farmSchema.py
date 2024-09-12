from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class FarmSchema(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    area_total: float
    latitud: Decimal
    longitud: Decimal 
    
class UpdateFarmSchema(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    area_total: Optional[float] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    
  