from pydantic import BaseModel
from typing import Optional

class MaquinariaAgricolaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    costPerHour: float

class MaquinariaAgricolaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    costPerHour: Optional[float] = None

class MaquinariaAgricola(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    costPerHour: float

    class Config:
        orm_mode = True
