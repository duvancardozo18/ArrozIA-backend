from pydantic import BaseModel
from typing import Optional

class LaborCulturalBase(BaseModel):
    nombre: str
    descripcion: Optional[str]
    precio_hectaria: Optional[float]
    precio_hectaria_estimada: Optional[float]
    id_etapa_fenologica: Optional[int]  # Relación con PhenologicalStage

class LaborCulturalCreate(LaborCulturalBase):
    pass

class LaborCulturalUpdate(LaborCulturalBase):
    pass

class LaborCulturalResponse(LaborCulturalBase):
    id: int

    class Config:
        orm_mode = True
