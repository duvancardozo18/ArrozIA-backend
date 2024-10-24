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
    descripcion: Optional[str] = None  # Usa Optional en lugar de '|'
    unidad_id: int
    costo_unitario: float

class AgriculturalInputCreate(AgriculturalInputBase):
    pass

# Agrega el campo id aquí para devolverlo en las respuestas
class AgriculturalInput(AgriculturalInputBase):
    id: int  # Asegúrate de incluir este campo

    class Config:
        orm_mode = True

class AgriculturalInputUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_id: Optional[int] = None
    costo_unitario: Optional[float] = None

    class Config:
        orm_mode = True