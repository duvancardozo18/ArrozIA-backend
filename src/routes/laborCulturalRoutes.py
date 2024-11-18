from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.laborCulturalController import (
    create_labor_cultural,
    get_labores_culturales,
    get_labor_cultural_by_id,
    update_labor_cultural,
    delete_labor_cultural
)
from src.schemas.laborCulturalSchema import LaborCulturalCreate, LaborCulturalUpdate, LaborCulturalResponse
from src.database.database import get_db

LABOR_CULTURAL_ROUTES = APIRouter()

# Crear una nueva labor cultural
@LABOR_CULTURAL_ROUTES.post("/labor-cultural/create", response_model=LaborCulturalResponse)
async def create_labor(labor: LaborCulturalCreate, db: Session = Depends(get_db)):
    return create_labor_cultural(labor, db)

# Obtener todas las labores culturales
@LABOR_CULTURAL_ROUTES.get("/labor-cultural/read", response_model=list[LaborCulturalResponse])
async def read_labors(db: Session = Depends(get_db)):
    return get_labores_culturales(db)

# Obtener una labor cultural por ID
@LABOR_CULTURAL_ROUTES.get("/labor-cultural/read/{labor_id}", response_model=LaborCulturalResponse)
async def read_labor(labor_id: int, db: Session = Depends(get_db)):
    return get_labor_cultural_by_id(labor_id, db)

# Actualizar una labor cultural
@LABOR_CULTURAL_ROUTES.put("/labor-cultural/update/{labor_id}", response_model=LaborCulturalResponse)
async def update_labor(labor_id: int, labor: LaborCulturalUpdate, db: Session = Depends(get_db)):
    return update_labor_cultural(labor_id, labor, db)

# Eliminar una labor cultural
@LABOR_CULTURAL_ROUTES.delete("/labor-cultural/delete/{labor_id}")
async def delete_labor(labor_id: int, db: Session = Depends(get_db)):
    return delete_labor_cultural(labor_id, db)
