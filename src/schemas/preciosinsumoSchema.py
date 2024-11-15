from typing import Optional
from pydantic import BaseModel


class TipoInsumoSchema(BaseModel):
    id: Optional[int]  # Puede ser nulo
    nombre: Optional[str]  # Puede ser nulo


class AgriculturalInputWithTipoSchema(BaseModel):
    nombre: str
    descripcion: Optional[str]
    costo_unitario: float
    precio_unitario_estimado: Optional[float]
    cantidad_insumo: Optional[int]
    tipo_insumo: Optional[TipoInsumoSchema]  # Permite que tipo_insumo sea None

    class Config:
        orm_mode = True
