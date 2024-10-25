from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.controller.machineryController import create_machinery, get_machinery, get_all_machineries, update_machinery, delete_machinery
from src.schemas.machinerySchema import MaquinariaAgricola, MaquinariaAgricolaCreate, MaquinariaAgricolaUpdate
from src.database.database import get_db

MACHINERY_ROUTES = APIRouter()

# Crear una nueva maquinaria
@MACHINERY_ROUTES.post("/machinery/", response_model=MaquinariaAgricola, status_code=status.HTTP_201_CREATED)
def create_machinery_route(machinery: MaquinariaAgricolaCreate, db: Session = Depends(get_db)):
    return create_machinery(machinery, db)

# Obtener una maquinaria por ID
@MACHINERY_ROUTES.get("/machinery/{machinery_id}", response_model=MaquinariaAgricola)
def get_machinery_route(machinery_id: int, db: Session = Depends(get_db)):
    db_machinery = get_machinery(machinery_id, db)
    if db_machinery is None:
        raise HTTPException(status_code=404, detail="Machinery not found")
    return db_machinery

# Obtener todas las maquinarias
@MACHINERY_ROUTES.get("/machineries/", response_model=list[MaquinariaAgricola])
def get_all_machineries_route(db: Session = Depends(get_db)):
    return get_all_machineries(db)

# Actualizar una maquinaria
@MACHINERY_ROUTES.put("/machinery/{machinery_id}", response_model=MaquinariaAgricola)
def update_machinery_route(machinery_id: int, machinery: MaquinariaAgricolaUpdate, db: Session = Depends(get_db)):
    return update_machinery(machinery_id, machinery, db)

# Eliminar una maquinaria
@MACHINERY_ROUTES.delete("/machinery/{machinery_id}", response_model=dict)
def delete_machinery_route(machinery_id: int, db: Session = Depends(get_db)):
    return delete_machinery(machinery_id, db)
