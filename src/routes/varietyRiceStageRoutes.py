from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.varietyRiceStageController import (
    create_variety_rice_stage, get_variety_rice_stages, get_variety_rice_stage_by_id,
    update_variety_rice_stage, delete_variety_rice_stage
)
from src.database.database import get_session
from src.schemas.varietyRiceStageSchema import VarietyRiceStageCreate, VarietyRiceStageUpdate, VarietyRiceStageResponse

VARIETY_RICE_STAGE_ROUTES = APIRouter()

@VARIETY_RICE_STAGE_ROUTES.post("/variety-rice-stages", response_model=VarietyRiceStageResponse)
def create_stage_route(stage: VarietyRiceStageCreate, db: Session = Depends(get_session)):
    return create_variety_rice_stage(stage, db)

@VARIETY_RICE_STAGE_ROUTES.get("/variety-rice-stages", response_model=list[VarietyRiceStageResponse])
def get_stages_route(db: Session = Depends(get_session)):
    return get_variety_rice_stages(db)

@VARIETY_RICE_STAGE_ROUTES.get("/variety-rice-stages/{stage_id}", response_model=VarietyRiceStageResponse)
def get_stage_by_id_route(stage_id: int, db: Session = Depends(get_session)):
    stage = get_variety_rice_stage_by_id(stage_id, db)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage

@VARIETY_RICE_STAGE_ROUTES.put("/variety-rice-stages/{stage_id}", response_model=VarietyRiceStageResponse)
def update_stage_route(stage_id: int, stage: VarietyRiceStageUpdate, db: Session = Depends(get_session)):
    updated_stage = update_variety_rice_stage(stage_id, stage, db)
    if not updated_stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return updated_stage

@VARIETY_RICE_STAGE_ROUTES.delete("/variety-rice-stages/{stage_id}", response_model=VarietyRiceStageResponse)
def delete_stage_route(stage_id: int, db: Session = Depends(get_session)):
    deleted_stage = delete_variety_rice_stage(stage_id, db)
    if not deleted_stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return deleted_stage
