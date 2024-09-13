from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.landModel import Land

def get_lots_by_farm(farm_id: int, db: Session = Depends(get_db)):
    lots = db.query(Land).filter(Land.finca_id == farm_id).all()
    if not lots:
        raise HTTPException(status_code=404, detail="No lots found for the given farm ID")
    return lots
