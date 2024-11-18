from typing import Optional
from pydantic import BaseModel

class TipoInsumoSchema(BaseModel):
    id: Optional[int]  # Puede ser nulo
    nombre: Optional[str]  # Puede ser nulo

class AgriculturalInputWithTipoSchema(BaseModel):
    concepto: str  # Cambiado de "nombre" a "concepto"
    descripcion: Optional[str]
    valor_unitario: float  # Cambiado de "costo_unitario" a "valor_unitario"
    cantidad: Optional[int]  # Cambiado de "cantidad_insumo" a "cantidad"
    valor_total: float  # Nuevo campo para el total calculado
    tipo_insumo: Optional[TipoInsumoSchema]  # Permite que tipo_insumo sea None

    class Config:
        orm_mode = True
