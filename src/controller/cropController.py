from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.cropModel import Crop
from src.schemas.cropSchema import CropCreate, CropUpdate

def createCrop(crop: CropCreate, db: Session):
    db_crop = Crop(
        cropName=crop.cropName,
        varietyId=crop.varietyId,
        plotId=crop.plotId,
        plantingDate=crop.plantingDate,
        estimatedHarvestDate=crop.estimatedHarvestDate,
        actualHarvestDate=crop.actualHarvestDate,
        harvestedQuantity=crop.harvestedQuantity,
        weightUnitId=crop.weightUnitId,
        income=crop.income
    )
    
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    
    return db_crop

def getCrop(cropId: int, db: Session):
    crop = db.query(Crop).filter(Crop.id == cropId).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop

def getAllCrops(db: Session):
    crops = db.query(Crop).all()
    return crops

def updateCrop(cropId: int, cropUpdate: CropUpdate, db: Session):
    crop = db.query(Crop).filter(Crop.id == cropId).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    for key, value in cropUpdate.dict(exclude_unset=True).items():
        setattr(crop, key, value)
    
    db.commit()
    db.refresh(crop)
    return crop

def deleteCrop(cropId: int, db: Session):
    crop = db.query(Crop).filter(Crop.id == cropId).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    db.delete(crop)
    db.commit()
    return {"message": "Crop deleted successfully"}
