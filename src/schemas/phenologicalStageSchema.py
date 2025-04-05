# src/schemas/phenologicalStageSchema.py
from pydantic import BaseModel

class PhenologicalStageBase(BaseModel):
    nombre: str
    fase: str

class PhenologicalStageCreate(PhenologicalStageBase):
    pass

class PhenologicalStageUpdate(PhenologicalStageBase):
    pass

class PhenologicalStageResponse(PhenologicalStageBase):
    id: int

    class Config:
        orm_mode = True
