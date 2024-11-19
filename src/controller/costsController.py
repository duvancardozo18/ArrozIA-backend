from sqlalchemy.orm import Session
from src.models.costsModel import Costs
from src.schemas.costsSchema import CostsCreate, CostsUpdate


def create_cost(db: Session, cost_data: CostsCreate):
    cost = Costs(**cost_data.dict())
    db.add(cost)
    db.commit()
    db.refresh(cost)
    return cost


def get_costs_by_cultivo(db: Session, cultivo_id: int):
    return db.query(Costs).filter(Costs.cultivo_id == cultivo_id).all()


def get_cost_by_id(db: Session, cost_id: int):
    return db.query(Costs).filter(Costs.id == cost_id).first()


def update_cost(db: Session, cost_id: int, cost_data: CostsUpdate):
    cost = db.query(Costs).filter(Costs.id == cost_id).first()
    if not cost:
        return None

    for key, value in cost_data.dict(exclude_unset=True).items():
        setattr(cost, key, value)

    db.commit()
    db.refresh(cost)
    return cost


def delete_cost(db: Session, cost_id: int):
    cost = db.query(Costs).filter(Costs.id == cost_id).first()
    if not cost:
        return None

    db.delete(cost)
    db.commit()
    return cost
