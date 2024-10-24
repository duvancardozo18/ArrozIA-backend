from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.cropController import (
    createCrop, 
    getCrop, 
    updateCrop, 
    deleteCrop, 
    getAllCrops, 
    getCropInfo, 
    getCropsByLand  # Importar la nueva función
)
from src.database.database import get_session
from src.schemas.cropSchema import CropCreate, CropOut, CropUpdate

CROP_ROUTES = APIRouter()

# Ruta para crear un cultivo
@CROP_ROUTES.post("/crops", response_model=CropOut)
def createCropRoute(crop: CropCreate, db: Session = Depends(get_session)):
    return createCrop(crop, db)

# Ruta para obtener todos los cultivos (sin filtrar)
@CROP_ROUTES.get("/crops/all", response_model=list[CropOut])
def getAllCropsRoute(db: Session = Depends(get_session)):
    return getAllCrops(db)

# Nueva ruta para obtener cultivos por ID de lote (filtrados por plotId)
@CROP_ROUTES.get("/crops/by_land/{land_id}", response_model=list[CropOut])
def getCropsByLandRoute(land_id: int, db: Session = Depends(get_session)):
    return getCropsByLand(land_id, db)


# Ruta para obtener un cultivo específico por su ID
@CROP_ROUTES.get("/crops/{crop_id}", response_model=CropOut)
def getCropRoute(crop_id: int, db: Session = Depends(get_session)):
    return getCrop(crop_id, db)

# Ruta para actualizar un cultivo
@CROP_ROUTES.put("/crops/{crop_id}", response_model=CropOut)
def updateCropRoute(crop_id: int, crop: CropUpdate, db: Session = Depends(get_session)):
    return updateCrop(crop_id, crop, db)

# Ruta para eliminar un cultivo
@CROP_ROUTES.delete("/crops/{crop_id}")
def deleteCropRoute(crop_id: int, db: Session = Depends(get_session)):
    return deleteCrop(crop_id, db)

# Ruta para obtener información de un cultivo por slugs de finca, lote y cultivo
@CROP_ROUTES.get("/finca/{finca_slug}/lote/{lote_slug}/cultivo/{cultivo_slug}", response_model=CropOut)
def get_crop_route(finca_slug: str, lote_slug: str, cultivo_slug: str, db: Session = Depends(get_session)):
    return getCropInfo(finca_slug, lote_slug, cultivo_slug, db)

