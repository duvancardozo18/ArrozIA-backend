from pydantic import BaseModel
from typing import Optional

class VarietyArrozResponse(BaseModel):
    id: int
    nombre: str

class PhenologicalStageResponse(BaseModel):
    id: int
    nombre: str

class VarietyRiceStageBase(BaseModel):
    # Campos base sin incluir la relación directa variety_id, solo variety y phenological_stage
    etapa_fenologica_id: Optional[int] = None
    dias_duracion: Optional[int] = None
    nombre: Optional[str] = None

class VarietyRiceStageCreate(VarietyRiceStageBase):
    variedad_arroz_id: int

class VarietyRiceStageUpdate(VarietyRiceStageBase):
    variedad_arroz_id: Optional[int] = None

class VarietyRiceStageResponse(VarietyRiceStageBase):
    id: int
    variety: Optional[VarietyArrozResponse] = None
    phenological_stage: Optional[PhenologicalStageResponse] = None

    class Config:
            orm_mode = True