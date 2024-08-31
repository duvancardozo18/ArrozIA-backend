from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class LoteSchema(BaseModel):
    nombre: str
    finca_id: int
    area: float
    unidad_area_id: int
    latitud: Optional[Decimal]  
    longitud: Optional[Decimal] 

    class Config:
        orm_mode = True
        schema_extra = {
            'latitud': condecimal(max_digits=10, decimal_places=5),
            'longitud': condecimal(max_digits=10, decimal_places=5)
        }
