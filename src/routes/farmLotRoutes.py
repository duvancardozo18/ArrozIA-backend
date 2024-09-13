from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.farmLotSchema import FarmLotSchema
from src.controller.farmLotController import get_lots_by_farm
from src.database.database import get_db

FARM_LOT_ROUTES = APIRouter()

@FARM_LOT_ROUTES.get("/farmlots/farm/{farm_id}", response_model=list[FarmLotSchema])
def get_lots(farm_id: int, db: Session = Depends(get_db)):
    return get_lots_by_farm(farm_id, db)
