# src/controller/phenologicalStageController.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.phenologicalStageModel import PhenologicalStage
from src.schemas.phenologicalStageSchema import PhenologicalStageCreate, PhenologicalStageUpdate

def get_all_phenological_stages(session: Session):
    return session.query(PhenologicalStage).all()

def get_phenological_stage(stage_id: int, session: Session):
    stage = session.query(PhenologicalStage).filter(PhenologicalStage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Phenological Stage not found")
    return stage

def create_phenological_stage(stage_data: PhenologicalStageCreate, session: Session):
    new_stage = PhenologicalStage(**stage_data.dict())
    session.add(new_stage)
    session.commit()
    session.refresh(new_stage)
    return new_stage

def update_phenological_stage(stage_id: int, stage_data: PhenologicalStageUpdate, session: Session):
    stage = get_phenological_stage(stage_id, session)
    for key, value in stage_data.dict().items():
        setattr(stage, key, value)
    session.commit()
    session.refresh(stage)
    return stage

def delete_phenological_stage(stage_id: int, session: Session):
    stage = get_phenological_stage(stage_id, session)
    session.delete(stage)
    session.commit()
    return {"message": "Phenological Stage deleted"}
