from sqlalchemy.orm import Session
from src.models.varietyRiceStageModel import VarietyRiceStageModel
from src.schemas.varietyRiceStageSchema import VarietyRiceStageCreate, VarietyRiceStageUpdate
from sqlalchemy.orm import joinedload


def create_variety_rice_stage(stage: VarietyRiceStageCreate, db: Session):
    new_stage = VarietyRiceStageModel(**stage.dict())
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    return new_stage

def get_variety_rice_stages(db: Session):
    return db.query(VarietyRiceStageModel).options(
        joinedload(VarietyRiceStageModel.variety),  # Cambio aquí
        joinedload(VarietyRiceStageModel.phenological_stage)  # Y aquí
    ).all()

def get_variety_rice_stage_by_id(stage_id: int, db: Session):
    return db.query(VarietyRiceStageModel).filter(VarietyRiceStageModel.id == stage_id).first()

def update_variety_rice_stage(stage_id: int, stage: VarietyRiceStageUpdate, db: Session):
    db_stage = get_variety_rice_stage_by_id(stage_id, db)
    if db_stage:
        for key, value in stage.dict(exclude_unset=True).items():
            setattr(db_stage, key, value)
        db.commit()
        db.refresh(db_stage)
    return db_stage

def delete_variety_rice_stage(stage_id: int, db: Session):
    db_stage = get_variety_rice_stage_by_id(stage_id, db)
    if db_stage:
        db.delete(db_stage)
        db.commit()
    return db_stage
