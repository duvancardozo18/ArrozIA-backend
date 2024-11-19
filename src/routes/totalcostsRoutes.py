from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.controller.totalcostsController import get_total_costs, get_overall_total_cost
from src.schemas.totalcostsSchema import TotalCostsResponse, OverallTotalResponse

router = APIRouter()

#Trae el bodý del nombre y costos totales de cada uno
@router.get("/total-costs/{cultivo_id}", response_model=TotalCostsResponse, tags=["Costs"])
def get_total_costs_data(cultivo_id: int, db: Session = Depends(get_session)):
    """
    Retorna los costos del cultivo, insumos y labores culturales con conceptos quemados.
    """
    try:
        return get_total_costs(db, cultivo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Trae el costo total de todos los costos
@router.get("/overall-total/{cultivo_id}", response_model=OverallTotalResponse, tags=["Costs"])
def get_overall_total(cultivo_id: int, db: Session = Depends(get_session)):
    """
    Retorna el total general de costos de un cultivo.
    """
    try:
        return get_overall_total_cost(db, cultivo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))