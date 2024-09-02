from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.cultivoController import create_cultivo, get_cultivo, update_cultivo, delete_cultivo, get_all_cultivos
from src.database.database import get_session
from src.schemas.cultivoSchema import CultivoCreate, CultivoOut, CultivoUpdate

CULTIVO_ROUTES = APIRouter()

@CULTIVO_ROUTES.post("/cultivos", response_model=CultivoOut)
def create_cultivo_route(cultivo: CultivoCreate, db: Session = Depends(get_session)):
    return create_cultivo(cultivo, db)

@CULTIVO_ROUTES.get("/cultivos/{cultivo_id}", response_model=CultivoOut)
def get_cultivo_route(cultivo_id: int, db: Session = Depends(get_session)):
    return get_cultivo(cultivo_id, db)

@CULTIVO_ROUTES.get("/cultivos", response_model=list[CultivoOut])
def get_all_cultivos_route(db: Session = Depends(get_session)):
    return get_all_cultivos(db)

@CULTIVO_ROUTES.put("/cultivos/{cultivo_id}", response_model=CultivoOut)
def update_cultivo_route(cultivo_id: int, cultivo: CultivoUpdate, db: Session = Depends(get_session)):
    return update_cultivo(cultivo_id, cultivo, db)

@CULTIVO_ROUTES.delete("/cultivos/{cultivo_id}")
def delete_cultivo_route(cultivo_id: int, db: Session = Depends(get_session)):
    return delete_cultivo(cultivo_id, db)
