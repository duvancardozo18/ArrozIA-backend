from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, timedelta

router = APIRouter()

# Modelo de datos para recibir información del ciclo vegetativo
class CropCycleRequest(BaseModel):
    sowing_date: date
    variety: str

# Diccionario con las etapas fenológicas de referencia
CYCLE_STAGES = {
    "germination": 10,  # en días
    "tillering": 20,
    "elongation": 30,
    "heading": 40,
    "ripening": 50
}

@router.post("/generate-cycle", response_model=List[str])
async def generate_crop_cycle(cycle_request: CropCycleRequest):
    try:
        stages = []
        current_date = cycle_request.sowing_date
        
        for stage, days in CYCLE_STAGES.items():
            stage_end = current_date + timedelta(days=days)
            stages.append(f"Stage {stage}: Start: {current_date}, End: {stage_end}")
            current_date = stage_end
        
        return stages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating crop cycle")
