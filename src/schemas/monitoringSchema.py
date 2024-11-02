from pydantic import BaseModel, Field
from typing import Optional

class MonitoringBase(BaseModel):
    tipo: str = Field(..., max_length=100)
    variedad_arroz_etapa_fenologica_id: Optional[int]
    recomendacion: Optional[str]
    crop_id: int 

class MonitoringCreate(MonitoringBase):
    pass

class MonitoringUpdate(MonitoringBase):
    pass

class MonitoringOut(MonitoringBase):
    id: int
    etapaNombre: Optional[str] = None  # Agrega el campo opcional para el nombre de la etapa fenológica

    class Config:
        orm_mode = True
