from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.controller.landCropController import getCropsByLandId
from src.schemas.cropSchema import CropOut  # Usar CropOut en lugar de CropSchema

LAND_CROP_ROUTES = APIRouter()

@LAND_CROP_ROUTES.get("/land/{landId}", response_model=list[CropOut])  # Cambiar a CropOut
def getCrops(landId: int, db: Session = Depends(get_db)):
    return getCropsByLandId(landId, db)
