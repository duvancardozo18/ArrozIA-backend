from sqlalchemy.orm import Session
from src.models.cropModel import Crop
from src.models.landModel import Land

def get_crops_by_farm_id(farm_id: int, db: Session):
    crops = (
        db.query(Crop)
        .join(Land, Crop.plotId == Land.id)  # Cambia `plotId` si es necesario
        .filter(Land.finca_id == farm_id)  # Cambia `finca_id` al nombre correcto si es diferente
        .all()
    )
    return crops
