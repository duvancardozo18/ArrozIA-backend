# src/routes/phenologicalStageRoutes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.phenologicalStageController import (
    get_all_phenological_stages,
    get_phenological_stage,
    create_phenological_stage,
    update_phenological_stage,
    delete_phenological_stage
)
from src.database.database import get_session
from src.schemas.phenologicalStageSchema import (
    PhenologicalStageCreate,
    PhenologicalStageUpdate,
    PhenologicalStageResponse
)

PHENOLOGICAL_STAGE_ROUTES = APIRouter()

@PHENOLOGICAL_STAGE_ROUTES.get("/phenological-stages", response_model=list[PhenologicalStageResponse])
def get_stages_route(db: Session = Depends(get_session)):
    return get_all_phenological_stages(db)

@PHENOLOGICAL_STAGE_ROUTES.get("/phenological-stages/{stage_id}", response_model=PhenologicalStageResponse)
def get_stage_route(stage_id: int, db: Session = Depends(get_session)):
    return get_phenological_stage(stage_id, db)

@PHENOLOGICAL_STAGE_ROUTES.post("/phenological-stages", response_model=PhenologicalStageResponse)
def create_stage_route(stage_data: PhenologicalStageCreate, db: Session = Depends(get_session)):
    return create_phenological_stage(stage_data, db)

@PHENOLOGICAL_STAGE_ROUTES.put("/phenological-stages/{stage_id}", response_model=PhenologicalStageResponse)
def update_stage_route(stage_id: int, stage_data: PhenologicalStageUpdate, db: Session = Depends(get_session)):
    return update_phenological_stage(stage_id, stage_data, db)

@PHENOLOGICAL_STAGE_ROUTES.delete("/phenological-stages/{stage_id}", response_model=dict)
def delete_stage_route(stage_id: int, db: Session = Depends(get_session)):
    return delete_phenological_stage(stage_id, db)
