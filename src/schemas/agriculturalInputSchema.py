from typing import Optional
from pydantic import BaseModel

# Esquema de UnidadInsumo
class UnidadInsumoSchema(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

# Esquema de TipoInsumo
class TipoInsumoSchema(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

# Esquema base de AgriculturalInput
class AgriculturalInputBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo_unitario: float
    cantidad: float

class AgriculturalInputCreate(AgriculturalInputBase):
    unidad_id: int  # unidad_id se usa solo en la creación
    tipo_insumo_id: int  # tipo_insumo_id también se usa solo en la creación

class AgriculturalInput(AgriculturalInputBase):
    id: int
    unidad: Optional[UnidadInsumoSchema] = None  # Permitir que unidad sea None
    tipo_insumo: Optional[TipoInsumoSchema] = None  # Permitir que tipo_insumo sea None

    class Config:
        from_attributes = True

class AgriculturalInputUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_id: Optional[int] = None
    tipo_insumo_id: Optional[int] = None
    costo_unitario: Optional[float] = None
    cantidad: Optional[float] = None

    class Config:
        from_attributes = True
