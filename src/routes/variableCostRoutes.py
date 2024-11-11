from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List 
from src.database.database import get_db
from src.controller.variableCostController import create_variable_cost, get_variable_costs, get_variable_costs_details
from src.schemas.variableCostSchema import VariableCostsCreate, VariableCostsResponse

VARIABLE_COST_ROUTES = APIRouter()

# Crear un gasto variable
@VARIABLE_COST_ROUTES.post("/financial/variable-costs", response_model=VariableCostsResponse)
def create_variable_cost_route(variable_costs: VariableCostsCreate, db: Session = Depends(get_db)):
    return create_variable_cost(db, variable_costs)

# Obtener todos los gastos variables
@VARIABLE_COST_ROUTES.get("/financial/variable-costs", response_model=List[VariableCostsResponse])
def get_variable_costs_route(db: Session = Depends(get_db)):
    return get_variable_costs(db)

# Obtener detalles de los gastos variables
@VARIABLE_COST_ROUTES.get("/financial/variable-costs-details", response_model=List[VariableCostsResponse])
def get_variable_costs_details_route(db: Session = Depends(get_db)):
    return get_variable_costs_details(db)  # Llama a la nueva función
