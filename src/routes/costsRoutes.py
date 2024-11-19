from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_session
from src.controller.costsController import (
    create_cost,
    get_costs_by_cultivo,
    get_cost_by_id,
    update_cost,
    delete_cost,
)
from src.schemas.costsSchema import CostsCreate, CostsUpdate, CostsOut

router = APIRouter()


@router.post("/costs", response_model=CostsOut)
def create_new_cost(cost_data: CostsCreate, db: Session = Depends(get_session)):
    return create_cost(db, cost_data)


@router.get("/costs/{cultivo_id}", response_model=List[CostsOut])
def list_costs_by_cultivo(cultivo_id: int, db: Session = Depends(get_session)):
    return get_costs_by_cultivo(db, cultivo_id)


@router.get("/costs/details/{cost_id}", response_model=CostsOut)
def get_cost_details(cost_id: int, db: Session = Depends(get_session)):
    cost = get_cost_by_id(db, cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    return cost


@router.put("/costs/{cost_id}", response_model=CostsOut)
def update_existing_cost(cost_id: int, cost_data: CostsUpdate, db: Session = Depends(get_session)):
    updated_cost = update_cost(db, cost_id, cost_data)
    if not updated_cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    return updated_cost


@router.delete("/costs/{cost_id}", response_model=dict)
def delete_existing_cost(cost_id: int, db: Session = Depends(get_session)):
    deleted_cost = delete_cost(db, cost_id)
    if not deleted_cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    return {"message": "Cost deleted successfully"}
