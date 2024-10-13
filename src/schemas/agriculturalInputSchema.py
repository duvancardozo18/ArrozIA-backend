from typing import Optional

from pydantic import BaseModel


# Esquema de UniInput
class UniInputBase(BaseModel):
    nombre: str

class UniInputCreate(UniInputBase):
    pass

class UniInput(UniInputBase):
    id: int

    class Config:
        orm_mode = True
        
class UniInputUpdate(BaseModel):
    nombre: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema de AgriculturalInput
class AgriculturalInputBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    unidad_id: int
    costo_unitario: float

class AgriculturalInputCreate(AgriculturalInputBase):
    pass

# class AgriculturalInput(AgriculturalInputBase):
#     id: int
#     unidad: UniInput

    class Config:
        orm_mode = True
        
class AgriculturalInputUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_id: Optional[int] = None
    costo_unitario: Optional[float] = None

    class Config:
        orm_mode = True
