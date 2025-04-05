from pydantic import BaseModel
from typing import Optional

class LaborCulturalBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_hectaria: Optional[float]
    precio_hectaria_estimada: Optional[float]
    id_etapa_fenologica: Optional[int]  # Relación con PhenologicalStage

class LaborCulturalCreate(LaborCulturalBase):
    pass

class LaborCulturalUpdate(LaborCulturalBase):
    pass

class LaborCulturalResponse(LaborCulturalBase):
    id: int  # Incluir el ID en la respuesta
    precio_hora_real: Optional[float] = None  # Incluir precio_hora_real en la respuesta

    class Config:
            orm_mode = True

