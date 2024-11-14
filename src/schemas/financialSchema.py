from pydantic import BaseModel
from typing import List, Optional

# Respuesta para costos adicionales
class TotalAdditionalCostsResponse(BaseModel):
    total_additional_costs: float

# Respuesta para gastos financieros
class TotalFinancialExpensesResponse(BaseModel):
    total_financial_expenses: float

# Respuesta para costos de labores culturales
class RealLaborCostsResponse(BaseModel):
    nombre: str
    costo_total: float
    total_horas: int

class MachineryCostResponse(BaseModel):
    nombre: str
    costo_total: float
    total_horas: int

class AgriculturalInputCostsResponse(BaseModel):
    nombre: str
    costo_total: float
    total_cantidad: float

    class Config:
        orm_mode = True

# Respuesta general que incluya listas de cada tipo de costo
class AllCostsResponse(BaseModel):
    additional_costs: TotalAdditionalCostsResponse
    financial_expenses: TotalFinancialExpensesResponse
    labor_costs: List[RealLaborCostsResponse]
    machinery_costs: List[MachineryCostResponse]
    agricultural_input_costs: List[AgriculturalInputCostsResponse]


