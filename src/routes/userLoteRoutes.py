from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_session
from src.models.farmModel import Farm
from src.models.userFarmRoleModel import UserFarmRole
from src.models.landModel import Land  # Importa tu modelo de lotes
from src.schemas.landSchema import LandSchema  # Importa el esquema de lotes

USER_LOT_ROUTES = APIRouter()

@USER_LOT_ROUTES.get("/users/{user_id}/lots", response_model=list[LandSchema])
def get_user_lots(user_id: int, db: Session = Depends(get_session)):
    # Obtener fincas relacionadas con el usuario
    farms = db.query(Farm).join(UserFarmRole).filter(UserFarmRole.usuario_id == user_id).all()
    if not farms:
        raise HTTPException(status_code=404, detail="No farms found for this user")
    
    # Obtener lotes relacionados con esas fincas
    lots = db.query(Land).filter(Land.finca_id.in_([farm.id for farm in farms])).all()
    if not lots:
        raise HTTPException(status_code=404, detail="No lots found for this user")
    
    return lots
