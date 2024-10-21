from fastapi import APIRouter
from src.controller.cropCycleController import generate_crop_cycle


router = APIRouter()

# Definir las rutas para el ciclo vegetativo
router.post("/generate-cycle", response_model=list)(generate_crop_cycle)
