from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class FarmSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID de la finca")
    nombre: str
    ubicacion: str
    area_total: float
    latitud: Decimal
    longitud: Decimal 


class FincaResponseSchema(FarmSchema):
    id: Optional[int] = Field(None, description="ID de la finca")
    
class UpdateFarmSchema(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    area_total: Optional[float] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    
  