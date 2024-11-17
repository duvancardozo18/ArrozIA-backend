from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class HarvestBase(BaseModel):
    cultivo_id: int = Field(..., description="ID del cultivo relacionado")
    fecha_estimada_cosecha: Optional[date] = Field(None, description="Fecha estimada de cosecha")
    fecha_cosecha: Optional[date] = Field(None, description="Fecha de cosecha")
    precio_carga_mercado: float = Field(..., description="Precio por carga en el mercado")
    gasto_transporte_cosecha: float = Field(..., description="Gastos de transporte de la cosecha")
    gasto_recoleccion: float = Field(..., description="Gastos de recolección")
    cantidad_producida_cosecha: float = Field(..., description="Cantidad producida en la cosecha")
    venta_cosecha: float = Field(..., description="Total de venta de la cosecha")

    class Config:
        from_attributes = True

class HarvestCreate(HarvestBase):
    pass

class HarvestUpdate(BaseModel):
    cultivo_id: Optional[int]  # Permitir actualizar el cultivo_id
    fecha_estimada_cosecha: Optional[date]
    fecha_cosecha: Optional[date]
    precio_carga_mercado: Optional[float]
    gasto_transporte_cosecha: Optional[float]
    gasto_recoleccion: Optional[float]
    cantidad_producida_cosecha: Optional[float]
    venta_cosecha: Optional[float]

    class Config:
        from_attributes = True

class HarvestOut(HarvestBase):
    id: int = Field(..., description="ID de la cosecha")

    class Config:
        orm_mode = True