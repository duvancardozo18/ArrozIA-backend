from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.cropController import createCrop, getCrop, updateCrop, deleteCrop, getAllCrops
from src.database.database import get_session
from src.schemas.cropSchema import CropCreate, CropOut, CropUpdate

CROP_ROUTES = APIRouter()

@CROP_ROUTES.post("/crops", response_model=CropOut)
def createCropRoute(crop: CropCreate, db: Session = Depends(get_session)):
    return createCrop(crop, db)

@CROP_ROUTES.get("/crops", response_model=list[CropOut])
def getAllCropsRoute(db: Session = Depends(get_session)):
    return getAllCrops(db)

@CROP_ROUTES.get("/crops/{crop_id}", response_model=CropOut)
def getCropRoute(crop_id: int, db: Session = Depends(get_session)):
    return getCrop(crop_id, db)

@CROP_ROUTES.put("/crops/{crop_id}", response_model=CropOut)
def updateCropRoute(crop_id: int, crop: CropUpdate, db: Session = Depends(get_session)):
    return updateCrop(crop_id, crop, db)

@CROP_ROUTES.delete("/crops/{crop_id}")
def deleteCropRoute(crop_id: int, db: Session = Depends(get_session)):
    return deleteCrop(crop_id, db)
