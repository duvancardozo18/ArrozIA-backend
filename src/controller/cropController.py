from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.cropModel import Crop
from src.schemas.cropSchema import CropCreate, CropUpdate
from src.models.landModel import Land
from src.models.varietyArrozModel import VariedadArroz

def createCrop(crop: CropCreate, db: Session):
    db_crop = Crop(
        cropName=crop.cropName,
        varietyId=crop.varietyId,
        plotId=crop.plotId,
        plantingDate=crop.plantingDate,
        estimatedHarvestDate=crop.estimatedHarvestDate,
     
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

def getCropInfo(nombre_lote: str, nombre_cultivo: str, db: Session):
    # Eliminar espacios y saltos de línea adicionales
    nombre_lote = nombre_lote.strip()
    nombre_cultivo = nombre_cultivo.strip()
  
    # Buscar el lote por nombre
    lote = db.query(Land).filter(Land.nombre == nombre_lote).first()
 
    if not lote:
        raise HTTPException(status_code=404, detail="Lote not found")

    # Buscar el cultivo por nombre y lote

    cultivo = db.query(Crop).filter(Crop.plotId == lote.id, Crop.cropName == nombre_cultivo).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo not found")

    # Buscar la variedad de arroz asociada
    variedad = db.query(VariedadArroz).filter(VariedadArroz.id == cultivo.varietyId).first()
    if not variedad:
        raise HTTPException(status_code=404, detail="Variedad de arroz not found")

    return {
        "id": cultivo.id,
        "cropName": cultivo.cropName,
        "varietyId": variedad.id,
        "varietyName": variedad.nombre,
        "plotId": lote.id,
        "plotName": lote.nombre,
        "plantingDate": cultivo.plantingDate,
        "estimatedHarvestDate": cultivo.estimatedHarvestDate
    }
