from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.userFarmController import (
    create_user_farm, get_all_user_farms, getUserFarmRolById, update_user_farm_role_by_id, delete_user_farm
)
from src.database.database import get_session
from src.schemas.userFarmRoleSchema import UserFarmRoleShema, UserFarmRoleCreate, UserFarmRoleUpdate
from src.models.userFarmRoleModel import UserFarmRole
from src.models.farmModel import Farm

# Crear un enrutador específico para UserFarmRole
USER_FARM_ROUTES = APIRouter()

# Ruta para crear un registro de UserFarmRole
@USER_FARM_ROUTES.post("/user-farm", response_model=UserFarmRoleShema)
def create_user_farm_route(user_farm: UserFarmRoleCreate, db: Session = Depends(get_session)):
    return create_user_farm(user_farm, db)

# Ruta para obtener todos los registros de UserFarmRole
@USER_FARM_ROUTES.get("/users-farms-rol", response_model=list[UserFarmRoleShema])
def get_all_user_farms_route(db: Session = Depends(get_session)):
    return get_all_user_farms(db)

# Ruta para obtener un registro de UserFarmRole por ID de usuario
# @USER_FARM_ROUTES.get('/user-farm-rol/{user_id}', response_model=UserFarmRoleShema)
# def userFarmRol(user_id: int, session: Session = Depends(get_session)):
#     return getUserFarmRolById(user_id, session)



@USER_FARM_ROUTES.get('/user-farm-rol/{user_id}', response_model=UserFarmRoleShema)
def user_farm_role_with_farm(user_id: int, session: Session = Depends(get_session)):
    # Obtener el registro de UserFarmRole por el ID de usuario
    user_farm_role = session.query(UserFarmRole).filter(UserFarmRole.usuario_id == user_id).first()
    if not user_farm_role:
        raise HTTPException(status_code=404, detail="User farm role not found")
    
    # Obtener la finca relacionada usando la columna `finca_id` de `UserFarmRole`
    farm = session.query(Farm).filter(Farm.id == user_farm_role.finca_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    
    # Retornar el registro con el nombre de la finca, ajustando los nombres de los campos
    return {
        "usuario_id": user_farm_role.usuario_id,  
        "finca_id": user_farm_role.finca_id,     
        "farm_name": farm.nombre
    }

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
