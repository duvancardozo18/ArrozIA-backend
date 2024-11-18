from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.harvestController import (
    create_harvest,
    get_harvest,
    update_harvest,
    delete_harvest,
    get_all_harvests_by_crop,
)
from src.database.database import get_session
from src.schemas.harvestSchema import HarvestCreate, HarvestOut, HarvestUpdate

HARVEST_ROUTES = APIRouter()

@HARVEST_ROUTES.get("/harvest/crops/{cultivo_id}")
def list_harvests_by_crop(cultivo_id: int, db: Session = Depends(get_session)):
    try:
        return get_all_harvests_by_crop(db, cultivo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@HARVEST_ROUTES.get("/harvest/{cultivo_id}/{cosecha_id}")
def retrieve_harvest(cultivo_id: int, cosecha_id: int, db: Session = Depends(get_session)):
    try:
        return get_harvest(db, cultivo_id, cosecha_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@HARVEST_ROUTES.post("/harvest/", response_model=HarvestOut)
def create_new_harvest(harvest_data: HarvestCreate, db: Session = Depends(get_session)):
    try:
        return create_harvest(db, harvest_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@HARVEST_ROUTES.put("/harvest/{cultivo_id}/{cosecha_id}", response_model=HarvestOut)
def modify_harvest(cultivo_id: int, cosecha_id: int, update_data: HarvestUpdate, db: Session = Depends(get_session)):
    return update_harvest(db, cultivo_id, cosecha_id, update_data.dict(exclude_unset=True))

@HARVEST_ROUTES.delete("/harvest/{cultivo_id}/{cosecha_id}")
def remove_harvest(cultivo_id: int, cosecha_id: int, db: Session = Depends(get_session)):
    try:
        return delete_harvest(db, cultivo_id, cosecha_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))