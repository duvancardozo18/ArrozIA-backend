from pydantic import BaseModel
from typing import Optional

class LaborCulturalBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class LaborCulturalCreate(LaborCulturalBase):
    pass

class LaborCulturalUpdate(LaborCulturalBase):
    pass

class LaborCulturalResponse(LaborCulturalBase):
    id: int  # Incluir el ID en la respuesta
    precio_hora_real: Optional[float] = None  # Incluir precio_hora_real en la respuesta

    class Config:
        from_attributes = True
