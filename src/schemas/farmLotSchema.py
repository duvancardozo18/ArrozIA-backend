from pydantic import BaseModel
from typing import Optional

class FarmLotSchema(BaseModel):
    id: int
    nombre: str
    area: float
    latitud: Optional[float] = None  # Permitir None
    longitud: Optional[float] = None  # Permitir None

    class Config:
        orm_mode = True
