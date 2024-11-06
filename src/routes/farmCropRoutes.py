# src/routes/farmCropRoutes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.farmCropController import get_crops_by_farm_id
from src.database.database import get_session
from src.schemas.cropSchema import CropOut  # Define el esquema de salida para los cultivos

FARM_CROP_ROUTES = APIRouter()

@FARM_CROP_ROUTES.get("/farms/{farm_id}/crops", response_model=list[CropOut])
def get_crops_for_farm(farm_id: int, db: Session = Depends(get_session)):
    crops = get_crops_by_farm_id(farm_id, db)
    if not crops:
        raise HTTPException(status_code=404, detail="No crops found for this farm")
    return crops
