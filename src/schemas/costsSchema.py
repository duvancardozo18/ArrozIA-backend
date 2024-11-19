from pydantic import BaseModel
from typing import Optional


class CostsBase(BaseModel):
    concepto: str
    descripcion: Optional[str]
    precio: float
    cultivo_id: int


class CostsCreate(CostsBase):
    pass


class CostsUpdate(BaseModel):
    concepto: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]


class CostsOut(CostsBase):
    id: int

    class Config:
        from_attributes = True
