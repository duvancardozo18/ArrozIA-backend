from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  
from src.database.database import get_db
from src.controller.financialController import (
    calculate_total_additional_costs,
    calculate_total_financial_expenses,
    calculate_total_estimated_additional_costs,
    calculate_total_estimated_financial_expenses,
    get_real_labor_costs,
    get_real_machinery_costs,
    get_real_agricultural_input_costs,
    get_estimated_labor_costs,
    get_estimated_machinery_costs_from_controller,
    get_estimated_agricultural_input_costs
)
from src.schemas.financialSchema import (
    TotalAdditionalCostsResponse,
    TotalFinancialExpensesResponse,
    RealLaborCostsResponse,
    MachineryCostResponse,
    AgriculturalInputCostsResponse
)

FINANCIAL_ROUTES = APIRouter()

# Costos Adicionales (Reales y Estimados)
@FINANCIAL_ROUTES.get("/financial/additional-costs", response_model=TotalAdditionalCostsResponse)
def get_total_additional_costs(db: Session = Depends(get_db)):
    total_additional_costs = calculate_total_additional_costs(db)
    return {"total_additional_costs": total_additional_costs}

@FINANCIAL_ROUTES.get("/financial/estimated-additional-costs", response_model=TotalAdditionalCostsResponse)
def get_total_estimated_additional_costs(db: Session = Depends(get_db)):
    total_estimated_additional_costs = calculate_total_estimated_additional_costs(db)
    return {"total_additional_costs": total_estimated_additional_costs}  # Cambiado a total_additional_costs

# Gastos Financieros (Reales y Estimados)
@FINANCIAL_ROUTES.get("/financial/financial-expenses", response_model=TotalFinancialExpensesResponse)
def get_total_financial_expenses(db: Session = Depends(get_db)):
    total_financial_expenses = calculate_total_financial_expenses(db)
    return {"total_financial_expenses": total_financial_expenses}

@FINANCIAL_ROUTES.get("/financial/estimated-financial-expenses", response_model=TotalFinancialExpensesResponse)
def get_total_estimated_financial_expenses(db: Session = Depends(get_db)):
    total_estimated_financial_expenses = calculate_total_estimated_financial_expenses(db)
    return {"total_financial_expenses": total_estimated_financial_expenses}  # Cambiado a total_financial_expenses

# Labores Culturales (Reales y Estimados)
@FINANCIAL_ROUTES.get("/financial/real-labor-costs", response_model=List[RealLaborCostsResponse])
def get_labor_costs(db: Session = Depends(get_db)):
    labor_costs = get_real_labor_costs(db)
    return labor_costs

@FINANCIAL_ROUTES.get("/financial/estimated-labor-costs", response_model=List[RealLaborCostsResponse])
def get_estimated_labor_costs_route(db: Session = Depends(get_db)):
    estimated_labor_costs = get_estimated_labor_costs(db)  # Asegúrate de usar la función correcta del controlador
    return estimated_labor_costs

# Costos de Maquinaria (Reales y Estimados)
@FINANCIAL_ROUTES.get("/financial/machinery-costs", response_model=List[MachineryCostResponse])
def get_machinery_costs(db: Session = Depends(get_db)):
    machinery_costs = get_real_machinery_costs(db)
    return machinery_costs

@FINANCIAL_ROUTES.get("/financial/estimated-machinery-costs", response_model=List[MachineryCostResponse])
def get_estimated_machinery_costs(db: Session = Depends(get_db)):
    estimated_machinery_costs = get_estimated_machinery_costs_from_controller(db)  # Cambia el nombre aquí
    return estimated_machinery_costs


# Costos de Insumos Agrícolas (Reales y Estimados)
@FINANCIAL_ROUTES.get("/financial/agricultural-input-costs", response_model=List[AgriculturalInputCostsResponse])
def get_agricultural_input_costs(db: Session = Depends(get_db)):
    agricultural_input_costs = get_real_agricultural_input_costs(db)
    return agricultural_input_costs

@FINANCIAL_ROUTES.get("/financial/estimated-agricultural-input-costs", response_model=List[AgriculturalInputCostsResponse])
def get_estimated_agricultural_input_costs_route(db: Session = Depends(get_db)):
    estimated_agricultural_input_costs = get_estimated_agricultural_input_costs(db)  # Llama la función del controlador
    return estimated_agricultural_input_costs
