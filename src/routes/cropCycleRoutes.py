from fastapi import APIRouter, HTTPException
from src.controller.cropCycleController import generateCropCycle
from src.schemas.cropCycleSchemas import CropCycleRequest, CropCycleStageResponse

CROP_CYCLE_ROUTES = APIRouter(prefix="/crop-cycle")

@CROP_CYCLE_ROUTES.post("/generate-cycle", response_model=list[CropCycleStageResponse])
async def generate_crop_cycle(cycle_request: CropCycleRequest):
    try:
        return generateCropCycle(cycle_request.sowingDate)
    except HTTPException as e:
        raise e
