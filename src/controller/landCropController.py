from sqlalchemy.orm import Session
from src.models.cropModel import Crop

def getCropsByLandId(landId: int, db: Session):
    crops = db.query(Crop).filter(Crop.plotId == landId).all()
    return crops
