from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from src.controller.userFarmController import (
    create_user_farm, get_all_user_farms, getUserFarmRolById, update_user_farm_role_by_id, delete_user_farm
)
from src.database.database import get_session
from src.schemas.userFarmRoleSchema import UserFarmRoleShema, UserFarmRoleCreate, UserFarmRoleUpdate, AssignFarmRequest, FarmSchema
from src.models.userFarmRoleModel import UserFarmRole
from src.models.farmModel import Farm
from sqlalchemy.exc import IntegrityError
from typing import List

# Crear un enrutador específico para UserFarmRole
USER_FARM_ROUTES = APIRouter()

@USER_FARM_ROUTES.post("/users/{user_id}/assign-farm", response_model=UserFarmRoleShema)
def assign_farm_to_user(user_id: int, request: AssignFarmRequest, db: Session = Depends(get_session)):
    user_farm = UserFarmRoleCreate(usuario_id=user_id, finca_id=request.farm_id)
    
    try:
        # Intenta asignar la finca al usuario
        return create_user_farm(user_farm, db)
    except IntegrityError:
        # Si ocurre una excepción de duplicidad, realiza un rollback y lanza un mensaje de error específico
        db.rollback()
        raise HTTPException(status_code=400, detail="El usuario ya está relacionado a esa finca.")

# Ruta para obtener todos los registros de UserFarmRole
@USER_FARM_ROUTES.get("/users-farms-rol", response_model=list[UserFarmRoleShema])
def get_all_user_farms_route(db: Session = Depends(get_session)):
    return get_all_user_farms(db)


@USER_FARM_ROUTES.get("/users/{user_id}/farms", response_model=List[FarmSchema])
def get_user_farms(user_id: int, db: Session = Depends(get_session)):
    # Filtra las fincas que están relacionadas al `user_id`
    farms = db.query(Farm).join(UserFarmRole).filter(UserFarmRole.usuario_id == user_id).all()
    if not farms:
        raise HTTPException(status_code=404, detail="No farms found for this user")
    return farms
    
# Ruta para obtener un registro de UserFarmRole por ID de usuario
@USER_FARM_ROUTES.get('/user-farms/{user_id}', response_model=list[FarmSchema])
def get_user_farms(user_id: int, session: Session = Depends(get_session)):
    # Consulta todas las fincas relacionadas con el usuario especificado
    user_farms = (
        session.query(Farm)
        .join(UserFarmRole, UserFarmRole.finca_id == Farm.id)
        .filter(UserFarmRole.usuario_id == user_id)
        .all()
    )
    
    if not user_farms:
        raise HTTPException(status_code=404, detail="No farms found for this user")
    
    return user_farms

# Ruta para actualizar un registro de UserFarmRole
@USER_FARM_ROUTES.put('/user-farm/update/{user_id}', response_model=UserFarmRoleShema)
def update_user_farm_role_route(user_id: int, updated_data: UserFarmRoleUpdate, session: Session = Depends(get_session)):
    return update_user_farm_role_by_id(user_id, updated_data, session)

# Ruta para eliminar un registro de UserFarmRole
@USER_FARM_ROUTES.delete("/user-farm/{usuario_id}/{finca_id}")
def delete_user_farm_route(usuario_id: int, finca_id: int, db: Session = Depends(get_session)):
    if not delete_user_farm(usuario_id, finca_id, db):
        raise HTTPException(status_code=404, detail="UserFarmRole not found")
    return {"message": "UserFarmRole deleted successfully"}
