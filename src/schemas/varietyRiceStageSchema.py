from pydantic import BaseModel
from typing import Optional

class VarietyRiceStageBase(BaseModel):
    variedad_arroz_id: int
    etapa_fenologica_id: Optional[int] = None
    dias_duracion: Optional[int] = None
    nombre: Optional[str] = None

class VarietyRiceStageCreate(VarietyRiceStageBase):
    pass

class VarietyRiceStageUpdate(VarietyRiceStageBase):
    pass

class VarietyRiceStageResponse(VarietyRiceStageBase):
    id: int

    class Config:
        from_attributes = True
