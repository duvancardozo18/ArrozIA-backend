from pydantic import BaseModel
from typing import List, Optional

# Esquema para la creación de un nuevo gasto variable
class VariableCostsCreate(BaseModel):
    id_costos_adicionales: int  # Relación con la tabla costos_adicionales
    id_agua: int  # Relación con la tabla agua
    id_gastos_administrativos_financieros: int  # Relación con la tabla gastos_administrativos_financieros
    descripcion: Optional[str] = None  # Descripción opcional

    class Config:
        orm_mode = True

# Esquema para la respuesta de los gastos variables
class VariableCostsResponse(BaseModel):
    id: int
    descripcion: Optional[str] = None  # Descripción opcional
    costos_adicionales_nombre: Optional[float] = 0.0  # Permite None y asigna 0.0 por defecto
    agua_consumo: Optional[float] = 0.0  # Permite None y asigna 0.0 por defecto
    gastos_administrativos_impuesto: Optional[float] = 0.0  # Permite None y asigna 0.0 por defecto
    agua_consumo_energia: Optional[float] = 0.0  # Permite None y asigna 0.0 por defecto

    class Config:
        orm_mode = True


# Esquema para los detalles de los gastos variables (resumen de costos)
class VariableCostsDetailsResponse(BaseModel):
    id: int
    costos_adicionales_nombre: str  # Nombre del costo adicional
    agua_consumo: float  # Consumo de agua
    gastos_administrativos_impuesto: float  # Impuesto de los gastos administrativos

    class Config:
        orm_mode = True

