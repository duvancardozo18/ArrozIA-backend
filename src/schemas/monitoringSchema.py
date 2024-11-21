# from pydantic import BaseModel, Field
# from typing import Optional

# class MonitoringBase(BaseModel):
#     tipo: str = Field(..., max_length=100)
#     variedad_arroz_etapa_fenologica_id: Optional[int]
#     recomendacion: Optional[str]
#     crop_id: int 

# class MonitoringCreate(MonitoringBase):
#     pass

# class MonitoringUpdate(MonitoringBase):
#     pass

# class MonitoringOut(MonitoringBase):
#     id: int
#     etapaNombre: Optional[str] = None  # Agrega el campo opcional para el nombre de la etapa fenológica

#     class Config:
#         orm_mode = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class MonitoringBase(BaseModel):
    tipo: str = Field(..., max_length=100)
    variedad_arroz_etapa_fenologica_id: Optional[int]
    recomendacion: Optional[str]
    crop_id: int
    fecha_programada: date  # Campo obligatorio para la fecha programada
    fecha_finalizacion: Optional[date] = None  # Campo opcional para la fecha de finalización
    estado: int = Field(1, ge=1, le=2)  # Estado con valores restringidos (1: Pendiente, 2: Terminado)

class MonitoringCreate(MonitoringBase):
    pass

class MonitoringUpdate(MonitoringBase):
    pass

class MonitoringOut(MonitoringBase):
    id: int
    etapaNombre: Optional[str] = None  # Campo opcional para el nombre de la etapa fenológica

    class Config:
        orm_mode = True

class CompleteMonitoringRequest(BaseModel):
    fecha_finalizacion: date